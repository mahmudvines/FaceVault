# 👁 FaceVault — Local Face Recognition System

> Organize thousands of photos by person. 100% offline. No cloud. No API keys. Your data never leaves your machine.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-purple?style=flat-square)

---

## ✨ Features

- 🔍 **Automatic face detection** across any folder of images
- 👤 **Clusters faces** — groups all photos of the same person together
- 🏷 **Interactive naming UI** — click a person, see their photos, type a name
- 📁 **Auto-sort** — copies photos into `PersonName/0001.jpg`, `0002.jpg`…
- 🖼 **Things Images** — photos with no people go into a separate folder automatically
- ♻️ **Incremental** — re-run anytime, only new images are processed
- 🔒 **100% local** — no internet, no cloud, no data shared anywhere
- 🌐 **Beautiful web UI** — runs in your browser, feels like a native app

---

## 🚀 Quick Start

### 1. Install Python 3.11 or 3.12
Download from [python.org](https://www.python.org/downloads/) — tick **"Add to PATH"** during install.

> FaceVault is not compatible with Python 3.14 or newer. Use Python 3.11 or 3.12.

### 2. Run the launcher

**Windows:** Double-click `Launch_FaceVault.bat`

**Mac/Linux:**
```bash
chmod +x launch_facevault.sh
./launch_facevault.sh
```

Browser opens automatically at `http://localhost:5050`

### Or install manually:
```bash
pip install -r requirements.txt
python app.py
```

---

## 📖 How to Use

1. **Scan** — paste your photos folder path and click **Scan**
2. **Name** — click any detected person card, see their photos, type their name
3. **Sort** — click **Sort** to copy photos into named folders
4. **Done** — find sorted photos in the `sorted_by_person/` folder

Already-named people are remembered forever in `facevault_db.json`.

---

## 📁 Output Structure

```
FaceVault/
├── sorted_by_person/
│   ├── Alice/
│   │   ├── 0001.jpg
│   │   ├── 0002.jpg
│   │   └── ...
│   ├── Bob/
│   └── ...
├── Things Images/
│   └── ...          ← landscapes, objects, no faces
└── facevault_db.json  ← your permanent face database
```

---

## 🔒 Privacy

- Everything runs on **your own computer**
- No internet connection needed after install
- `facevault_db.json` is a local file — **you own it**
- Original photos are **never moved or deleted**
- Delete `facevault_db.json` anytime to wipe all face data

---

## ⚙️ Configuration

Edit `app.py` to tune accuracy:
```python
TOLERANCE = 0.50   # 0.40 = strict (fewer false matches), 0.60 = loose (more matches)
```

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Face Detection | `face_recognition` (dlib) |
| Backend | Python + Flask |
| Frontend | Vanilla HTML / CSS / JS |
| Database | Local JSON file |

---

## 📜 License

MIT — free to use, modify, and share.

---

*Built for privacy. Your photos, your machine, your control.*
