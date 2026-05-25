import sys
import os
import json
import shutil
import base64
import threading
import webbrowser
from pathlib import Path

if sys.version_info >= (3, 14):
    print("ERROR: FaceVault is not compatible with Python 3.14 or newer.")
    print(f"Detected Python {sys.version_info.major}.{sys.version_info.minor}.")
    print("Please run FaceVault with Python 3.11 or 3.12.")
    sys.exit(1)

from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
import numpy as np

app = Flask(__name__)

DB_FILE = "facevault_db.json"
SORTED_DIR = r"D:\ahbab\Education\Face app\FaceVault\Sorted images"
THINGS_DIR = os.path.join(SORTED_DIR, "Things Images")
TOLERANCE = 0.50

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled exception")
    return jsonify({"error": str(e)}), 500

# ── DB helpers ────────────────────────────────────────────────────────────────

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"clusters": [], "processed_files": [], "next_id": 1}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    db = load_db()
    total_people = len(db["clusters"])
    named = sum(1 for c in db["clusters"] if c.get("name") and c["name"] != "Unknown")
    total_photos = sum(len(c.get("photos", [])) for c in db["clusters"])
    return jsonify({
        "total_people": total_people,
        "named_people": named,
        "unnamed_people": total_people - named,
        "total_photos": total_photos,
        "processed_files": len(db.get("processed_files", []))
    })

@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.json
    folder = data.get("folder", "").strip()
    if not folder or not os.path.isdir(folder):
        return jsonify({"error": "Invalid folder path"}), 400

    try:
        import face_recognition
    except ImportError:
        return jsonify({"error": "face_recognition not installed. Run: pip install face_recognition"}), 500

    try:
        db = load_db()
        processed = set(db.get("processed_files", []))

        exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        all_images = [
            str(p) for p in Path(folder).rglob("*")
            if p.suffix.lower() in exts
        ]
        new_images = [img for img in all_images if img not in processed]

        added = 0
        no_face = []

        for img_path in new_images:
            try:
                image = face_recognition.load_image_file(img_path)
                locations = face_recognition.face_locations(image)
                encodings = face_recognition.face_encodings(image, locations)

                if not encodings:
                    no_face.append(img_path)
                    processed.add(img_path)
                    continue

                for enc in encodings:
                    matched = False
                    for cluster in db["clusters"]:
                        known = [np.array(e) for e in cluster.get("encodings", [])]
                        if known and face_recognition.compare_faces(known, enc, tolerance=TOLERANCE)[0]:
                            cluster["photos"].append(img_path)
                            cluster["encodings"].append(enc.tolist())
                            matched = True
                            break
                    if not matched:
                        db["clusters"].append({
                            "id": db["next_id"],
                            "name": "",
                            "photos": [img_path],
                            "encodings": [enc.tolist()]
                        })
                        db["next_id"] += 1

                processed.add(img_path)
                added += 1
            except Exception as e:
                app.logger.exception(f"Failed scanning image: {img_path}")
                processed.add(img_path)

        db["processed_files"] = list(processed)
        db["no_face_images"] = db.get("no_face_images", []) + no_face
        save_db(db)

        return jsonify({
            "scanned": len(new_images),
            "added": added,
            "no_face": len(no_face),
            "clusters": len(db["clusters"])
        })
    except Exception as e:
        app.logger.exception("Scan endpoint failed")
        return jsonify({"error": f"Scan failed: {e}"}), 500

@app.route("/api/people")
def get_people():
    db = load_db()
    result = []
    for c in db["clusters"]:
        thumb = None
        if c.get("photos"):
            thumb = _make_thumb(c["photos"][0])
        result.append({
            "id": c["id"],
            "name": c.get("name", ""),
            "count": len(c.get("photos", [])),
            "thumbnail": thumb
        })
    result.sort(key=lambda x: x["count"], reverse=True)
    return jsonify(result)

@app.route("/api/person/<int:person_id>")
def get_person(person_id):
    db = load_db()
    for c in db["clusters"]:
        if c["id"] == person_id:
            photos = []
            for p in c["photos"][:20]:
                thumb = _make_thumb(p)
                if thumb:
                    photos.append({"path": p, "thumb": thumb})
            return jsonify({
                "id": c["id"],
                "name": c.get("name", ""),
                "count": len(c["photos"]),
                "photos": photos
            })
    return jsonify({"error": "Not found"}), 404

@app.route("/api/name", methods=["POST"])
def set_name():
    data = request.json
    person_id = data.get("id")
    name = data.get("name", "").strip()
    db = load_db()
    for c in db["clusters"]:
        if c["id"] == person_id:
            c["name"] = name
            save_db(db)
            return jsonify({"ok": True})
    return jsonify({"error": "Not found"}), 404

@app.route("/api/sort", methods=["POST"])
def sort_photos():
    data = request.json or {}
    output_dir = data.get("output_dir", "").strip()
    if output_dir:
        output_dir = os.path.abspath(os.path.expanduser(output_dir))
    else:
        output_dir = SORTED_DIR

    db = load_db()
    things_dir = os.path.join(output_dir, "Things Images")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(things_dir, exist_ok=True)

    total_copied = 0

    for cluster in db["clusters"]:
        name = cluster.get("name") or f"Person_{cluster['id']}"
        safe_name = "".join(
            c if c not in '\\/:*?"<>|' else '_' for c in name
        ).strip() or f"Person_{cluster['id']}"
        person_dir = os.path.join(output_dir, safe_name)
        os.makedirs(person_dir, exist_ok=True)
        for i, photo in enumerate(cluster.get("photos", []), 1):
            if os.path.exists(photo):
                ext = Path(photo).suffix
                dest = os.path.join(person_dir, f"{i:04d}{ext}")
                shutil.copy2(photo, dest)
                total_copied += 1

    for i, photo in enumerate(db.get("no_face_images", []), 1):
        if os.path.exists(photo):
            ext = Path(photo).suffix
            dest = os.path.join(things_dir, f"{i:04d}{ext}")
            shutil.copy2(photo, dest)

    return jsonify({"copied": total_copied, "output": os.path.abspath(output_dir)})

@app.route("/api/merge", methods=["POST"])
def merge_people():
    data = request.json
    ids = data.get("ids", [])
    new_name = data.get("name", "")
    db = load_db()

    keep = None
    to_remove = []
    for c in db["clusters"]:
        if c["id"] in ids:
            if keep is None:
                keep = c
                keep["name"] = new_name
            else:
                keep["photos"].extend(c.get("photos", []))
                keep["encodings"].extend(c.get("encodings", []))
                to_remove.append(c["id"])

    db["clusters"] = [c for c in db["clusters"] if c["id"] not in to_remove]
    save_db(db)
    return jsonify({"ok": True})

@app.route("/api/delete/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    db = load_db()
    db["clusters"] = [c for c in db["clusters"] if c["id"] != person_id]
    save_db(db)
    return jsonify({"ok": True})

@app.route("/api/reset", methods=["POST"])
def reset_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    return jsonify({"ok": True})

def _make_thumb(photo_path, size=(200, 200)):
    try:
        with Image.open(photo_path) as img:
            img.thumbnail(size)
            if img.mode != "RGB":
                img = img.convert("RGB")
            import io
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=80)
            return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None

# ── Launch ────────────────────────────────────────────────────────────────────

def open_browser():
    import time
    time.sleep(1.2)
    webbrowser.open("http://localhost:5050")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    print("\n  ╔══════════════════════════════╗")
    print("  ║   FaceVault is running...    ║")
    print("  ║   http://localhost:5050      ║")
    print("  ║   Close window to stop.      ║")
    print("  ╚══════════════════════════════╝\n")
    app.run(host="0.0.0.0", port=5050, debug=False)
