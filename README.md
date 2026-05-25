# 👁️ FaceVault

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%202.x-black?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Privacy Badge](https://img.shields.io/badge/Privacy-100%25%20Local%20%2F%20Offline-purple?style=flat-square)](##-privacy--security)

FaceVault is an enterprise-grade, 100% offline local face recognition and photo organization system. Designed with a strict privacy-first architecture, it allows you to automatically detect, cluster, and sort thousands of local images by individual identities without relying on cloud APIs or external network dependencies.

---

## ✨ Key Features

* **Local Face Clustering & Tracking:** Utilizes deep learning to group matching faces automatically across large directory structures.
* **Non-Destructive Sorting Engine:** Organizes assets dynamically into dedicated identity directories while preserving the integrity of original source files.
* **Isolated Object Classification:** Automatically filters landscapes, macro shots, and non-human assets into a designated `Things Images` repository.
* **Incremental Processing Pipeline:** State-tracking allows re-scanning directories efficiently by skipping previously indexed media.
* **Web-Based Control Panel:** Fully local, responsive web UI designed for fluid identity labeling and gallery visualization.
* **Zero-Cloud Architecture:** Operates entirely edge-side; data telemetry or tracking layer does not exist.

---

## 🚀 Quick Start & Deployment

### Prerequisites
FaceVault requires **Python 3.11** or **Python 3.12**. 
> **Note:** Versions $\ge$ Python 3.14 are not supported due to upstream C++ compilation dependencies (`dlib`).

### Automated Setup

#### Windows
Double-click the pre-configured runtime script:
```bash
Launch_FaceVault.bat
