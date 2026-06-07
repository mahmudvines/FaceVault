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
from external_devices import get_device_manager
from simple_scanner import get_simple_scanner

app = Flask(__name__)

DB_FILE = "facevault_db.json"
SORTED_DIR = r"D:\ahbab\Education\Face app\FaceVault\Sorted images"
THINGS_DIR = os.path.join(SORTED_DIR, "Things Images")
TOLERANCE = 0.50

# Initialize device manager
device_manager = get_device_manager()

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
        print(f"[SCAN] Starting scan of: {folder}")
        db = load_db()
        processed = set(db.get("processed_files", []))
        
        print(f"[SCAN] Database loaded. Existing clusters: {len(db.get('clusters', []))}")

        # Use simple scanner - reliable and won't hang
        scanner = get_simple_scanner(tolerance=TOLERANCE, use_cnn=False)
        print(f"[SCAN] Scanner initialized. Finding images...")
        
        # Count all images first
        all_images = scanner.find_images(folder)
        new_images = [img for img in all_images if img not in processed]
        print(f"[SCAN] Found {len(all_images)} total images, {len(new_images)} new images to process")
        
        if new_images:
            added, no_face = scanner.scan_folder(folder, db, processed)
            print(f"[SCAN] Scanning complete. Added {added} faces, {len(no_face)} images with no faces")
        else:
            added = 0
            no_face = []
            print(f"[SCAN] No new images to process")

        db["processed_files"] = list(processed)
        db["no_face_images"] = db.get("no_face_images", []) + no_face
        
        print(f"[SCAN] Saving database with {len(db.get('clusters', []))} clusters...")
        save_db(db)
        print(f"[SCAN] Database saved successfully")

        scanned_count = len(all_images)
        cluster_count = len(db.get("clusters", []))
        
        print(f"[SCAN] Returning results: scanned={scanned_count}, added={added}, no_face={len(no_face)}, clusters={cluster_count}")

        return jsonify({
            "scanned": scanned_count,
            "added": added,
            "no_face": len(no_face),
            "clusters": cluster_count
        })
    except Exception as e:
        print(f"[SCAN ERROR] Exception: {type(e).__name__}: {str(e)}")
        app.logger.exception("Scan endpoint failed")
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500

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

# ── External Devices Routes ───────────────────────────────────────────────────

@app.route("/api/devices")
def get_devices():
    """Get all connected external devices"""
    try:
        print("[API] /api/devices - Getting devices")
        devices = device_manager.get_all_devices()
        print(f"[API] Found {len(devices)} devices: {devices}")
        return jsonify({
            "devices": devices,
            "count": len(devices)
        })
    except Exception as e:
        print(f"[API ERROR] Failed to get devices: {e}")
        app.logger.exception("Failed to get devices")
        return jsonify({"error": str(e)}), 500

@app.route("/api/devices/rescan", methods=["POST"])
def rescan_devices():
    """Rescan for connected devices"""
    try:
        print("[API] /api/devices/rescan - Starting rescan")
        device_manager.scan_devices()
        devices = device_manager.get_all_devices()
        print(f"[API] Rescan complete. Found {len(devices)} devices: {devices}")
        return jsonify({
            "devices": devices,
            "count": len(devices)
        })
    except Exception as e:
        print(f"[API ERROR] Failed to rescan devices: {e}")
        app.logger.exception("Failed to rescan devices")
        return jsonify({"error": str(e)}), 500

@app.route("/api/devices/favorites")
def get_favorites():
    """Get favorite devices"""
    try:
        favorites = device_manager.get_favorites()
        return jsonify({"favorites": favorites})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/devices/favorites/add", methods=["POST"])
def add_favorite():
    """Add device to favorites"""
    try:
        data = request.json
        mount_point = data.get("mount_point")
        label = data.get("label", "")
        
        if not mount_point:
            return jsonify({"error": "mount_point required"}), 400
        
        device_manager.add_favorite(mount_point, label)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/scan-external", methods=["POST"])
def scan_external():
    """Scan images from external device - optimized version"""
    data = request.json
    device_path = data.get("device_path", "").strip()
    
    if not device_path or not os.path.isdir(device_path):
        return jsonify({"error": "Invalid device path"}), 400
    
    try:
        import face_recognition
    except ImportError:
        return jsonify({"error": "face_recognition not installed. Run: pip install face_recognition"}), 500
    
    try:
        print(f"[EXTERNAL_SCAN] Starting scan of external device: {device_path}")
        db = load_db()
        processed = set(db.get("processed_files", []))
        
        # Use simple scanner - reliable and won't hang
        scanner = get_simple_scanner(tolerance=TOLERANCE, use_cnn=False)
        all_images = scanner.find_images(device_path)
        new_images = [img for img in all_images if img not in processed]
        print(f"[EXTERNAL_SCAN] Found {len(all_images)} total images, {len(new_images)} new images")
        
        if new_images:
            added, no_face = scanner.scan_folder(device_path, db, processed)
            print(f"[EXTERNAL_SCAN] Added {added} faces, {len(no_face)} no-face images")
        else:
            added = 0
            no_face = []
            print(f"[EXTERNAL_SCAN] No new images to process")

        db["processed_files"] = list(processed)
        db["no_face_images"] = db.get("no_face_images", []) + no_face
        print(f"[EXTERNAL_SCAN] Saving database...")
        save_db(db)

        scanned_count = len(all_images)
        cluster_count = len(db.get("clusters", []))

        return jsonify({
            "scanned": scanned_count,
            "added": added,
            "no_face": len(no_face),
            "clusters": cluster_count,
            "source": device_path
        })
    except Exception as e:
        print(f"[EXTERNAL_SCAN ERROR] Exception: {type(e).__name__}: {str(e)}")
        app.logger.exception("External scan failed")
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500

@app.route("/api/sort-to-external", methods=["POST"])
def sort_to_external():
    """Sort photos to external device"""
    data = request.json or {}
    output_dir = data.get("output_dir", "").strip()
    
    if not output_dir or not os.path.isdir(output_dir):
        return jsonify({"error": "Invalid output directory"}), 400
    
    try:
        # Check if we have write permissions
        if not os.access(output_dir, os.W_OK):
            return jsonify({"error": "No write permissions on device"}), 403
        
        db = load_db()
        things_dir = os.path.join(output_dir, "Things Images")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(things_dir, exist_ok=True)
        
        total_copied = 0
        errors = []
        
        for cluster in db["clusters"]:
            name = cluster.get("name") or f"Person_{cluster['id']}"
            safe_name = "".join(
                c if c not in '\\/:*?"<>|' else '_' for c in name
            ).strip() or f"Person_{cluster['id']}"
            person_dir = os.path.join(output_dir, safe_name)
            os.makedirs(person_dir, exist_ok=True)
            
            for i, photo in enumerate(cluster.get("photos", []), 1):
                if os.path.exists(photo):
                    try:
                        ext = Path(photo).suffix
                        dest = os.path.join(person_dir, f"{i:04d}{ext}")
                        shutil.copy2(photo, dest)
                        total_copied += 1
                    except Exception as e:
                        errors.append(f"{photo}: {str(e)}")
        
        # Copy images with no faces
        for i, photo in enumerate(db.get("no_face_images", []), 1):
            if os.path.exists(photo):
                try:
                    ext = Path(photo).suffix
                    dest = os.path.join(things_dir, f"{i:04d}{ext}")
                    shutil.copy2(photo, dest)
                except Exception as e:
                    errors.append(f"{photo}: {str(e)}")
        
        return jsonify({
            "copied": total_copied,
            "output": os.path.abspath(output_dir),
            "errors": errors,
            "error_count": len(errors)
        })
    except Exception as e:
        app.logger.exception("External sort failed")
        return jsonify({"error": f"Sort failed: {e}"}), 500

@app.route("/api/devices/images", methods=["POST"])
def list_device_images():
    """List images on external device"""
    data = request.json
    device_path = data.get("device_path", "").strip()
    
    if not device_path or not os.path.isdir(device_path):
        return jsonify({"error": "Invalid device path"}), 400
    
    try:
        exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        images = []
        
        for p in Path(device_path).rglob("*"):
            if p.suffix.lower() in exts and os.path.isfile(str(p)):
                images.append({
                    "path": str(p),
                    "size": os.path.getsize(str(p)),
                    "name": p.name
                })
        
        return jsonify({
            "images": images[:100],  # Limit to first 100 for performance
            "total": len(images),
            "device_path": device_path
        })
    except Exception as e:
        app.logger.exception("Failed to list device images")
        return jsonify({"error": str(e)}), 500

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
