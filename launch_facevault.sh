#!/bin/bash
clear
echo ""
echo "  ╔══════════════════════════════════════════╗"
echo "  ║         👁  FaceVault Launcher            ║"
echo "  ║   100% offline face recognition app      ║"
echo "  ╚══════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Find python
PYTHON=""
for cmd in python3.11 python3.12 python3.10 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "  [ERROR] Python not found!"
    echo ""
    echo "  Please install Python 3.11+ from: https://www.python.org/downloads/"
    exit 1
fi

echo "  [OK] Using: $PYTHON ($($PYTHON --version))"
echo ""
echo "  Installing/checking dependencies..."
$PYTHON -m pip install flask pillow numpy tqdm --quiet --upgrade

# Check face_recognition separately (heavier install)
if ! $PYTHON -c "import face_recognition" &>/dev/null; then
    echo "  Installing face_recognition (this may take a few minutes)..."
    $PYTHON -m pip install face_recognition
fi

echo ""
echo "  ══════════════════════════════════════════"
echo "   Starting FaceVault at http://localhost:5050"
echo "   Browser will open automatically."
echo "   Press Ctrl+C to stop."
echo "  ══════════════════════════════════════════"
echo ""

$PYTHON start.py
