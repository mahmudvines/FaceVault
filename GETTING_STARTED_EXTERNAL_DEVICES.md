# 🎯 FaceVault External Devices - Getting Started

## What's New?

FaceVault now supports **external devices**! You can:
- 📱 Scan photos directly from your phone, tablet, or camera
- 💾 Scan from USB drives and SD cards
- 🖥️ Organize photos to external hard drives
- 📊 See device info (space, type, accessibility)

---

## 🚀 Quick Start (5 minutes)

### 1. Connect Your Device
Plug in your USB drive, SD card, or connect your phone via USB cable.

### 2. Start FaceVault
**Windows**: Double-click `Launch_FaceVault.bat`  
**Mac/Linux**: Run `./launch_facevault.sh` or `python app.py`

### 3. Click "🔍 Scan Devices"
In the left sidebar under "💾 External Devices"

### 4. Select Your Device
The modal will show all connected devices with:
- Device name and type (USB, SD card, phone, etc.)
- Available space
- Whether it's accessible

### 5. Choose What To Do

**Option A: Import Photos From Device**
```
Select device → Click "🔍 Scan Selected"
→ FaceVault analyzes faces
→ Photos stay on device (original + backup)
```

**Option B: Save Organized Photos To Device**
```
(First organize your photos locally)
Select device → Click "💾 Sort to Device"  
→ Organized folders created on device
→ Device:/
   ├── Alice/
   ├── Bob/
   └── Things Images/
```

---

## 📱 Device-Specific Tips

### iPhone
1. Connect via USB cable
2. Tap "Trust" when prompted on phone
3. Device appears as "📱 iPhone"
4. No need to unlock (File app handles access)

### Android
1. Connect via USB cable
2. Swipe notification panel (top of screen)
3. Tap USB notification → "File Transfer"
4. Device appears as "📱 [Phone Name]"
5. Keep phone unlocked during operation

### USB Drive / Pen Drive
1. Plug into USB port
2. Windows: Should appear as drive letter (D:\, E:\, etc.)
3. Mac: Click Finder → should appear in sidebar
4. Linux: Should mount automatically in /media or /mnt

### SD Card
1. Insert into SD card reader
2. Connect reader via USB
3. Should appear as "💿 [Card Name]"
4. Typically contains: `/DCIM` or `/Pictures` folders

### External Hard Drive
1. Connect via USB
2. Should appear as "🖥 [Drive Name]"
3. Large drives may take 5-10 seconds to mount

---

## ⚙️ How Device Detection Works

### Windows
- Scans all drive letters (C: through Z:)
- Detects removable drives (USB, SD cards)
- Detects external fixed drives (external HDDs)

### macOS
- Scans `/Volumes` directory
- Shows all mounted external drives

### Linux
- Checks `/media` directory (user-mounted)
- Checks `/mnt` directory (system-mounted)

---

## 🎯 Common Workflows

### Workflow 1: Phone → Organize → USB
```
1. Connect iPhone/Android
2. "🔍 Scan Selected" → FaceVault processes photos
3. Name people in web UI
4. Plug in USB drive
5. "💾 Sort to Device" → Photos organized on USB
```

### Workflow 2: SD Card → PC → External HDD
```
1. Connect SD card (from camera)
2. "🔍 Scan Selected" → Analyze photos
3. Connect external hard drive
4. "💾 Sort to Device" → Backup organized photos
```

### Workflow 3: Consolidate Multiple Devices
```
1. Scan USB drive → 300 photos
2. Scan SD card → 500 photos
3. Scan phone → 200 photos
4. Total: 1000 photos, ~25 people detected
5. Connect external HDD
6. "💾 Sort to Device" → All organized on HDD
```

---

## ❌ Device Not Showing?

### Quick Fixes
1. **Wait 2-3 seconds** — Devices take time to mount
2. **Try Different Port** — Some USB ports are finicky
3. **Refresh Browser** — Press F5
4. **Restart App** — Close and reopen FaceVault
5. **Restart Computer** — For stubborn connections

### Still Not Working?
See: `TROUBLESHOOTING_EXTERNAL_DEVICES.md`

---

## 📂 Manual Path Entry

If device doesn't appear in modal, you can type the path directly:

### Windows
In "Scan Folder" field, type:
- `D:\` or `D:\DCIM` (for SD card)
- `E:\` (for second USB drive)
- `F:\Pictures` (specific folder)

Then click "Scan"

### macOS
In "Scan Folder" field, type:
- `/Volumes/USB_DRIVE`
- `/Volumes/SD_CARD/DCIM`
- `/Volumes/iPhone/DCIM`

Then click "Scan"

### Linux
In "Scan Folder" field, type:
- `/media/username/DEVICE_NAME`
- `/mnt/usb`
- `/mnt/sd_card`

Then click "Scan"

---

## 💾 Sorting TO Device

When you click "💾 Sort to Device", the app will:

1. Read your face database
2. Create folders on device:
   ```
   [Device]:/
   ├── Alice/           (all photos of Alice)
   │   ├── 0001.jpg
   │   ├── 0002.jpg
   │   └── ...
   ├── Bob/
   ├── Charlie/
   └── Things Images/   (photos with no faces)
   ```

3. **Copy** all organized photos to device
4. Original photos stay on your computer

⚠️ **Important**: Ensure device has enough space!
- Organized photos need as much space as originals
- Plus 10-20% buffer for safety

---

## 🔐 Privacy

✅ **100% Local Processing**
- All face detection happens on YOUR computer
- No data sent to cloud or external servers
- Devices accessed only locally

✅ **Device Access**
- You decide which device to scan
- Photos copied only if you click "Sort to Device"
- No automatic syncing

✅ **Database Storage**
- Database file (`facevault_db.json`) stored locally
- Can optionally copy to external device
- Nothing shared without your explicit action

---

## 📖 Full Documentation

For detailed information, see:

1. **[EXTERNAL_DEVICES_GUIDE.md](EXTERNAL_DEVICES_GUIDE.md)**
   - Complete feature guide
   - Device-specific instructions
   - Advanced workflows
   - Privacy & security notes

2. **[TROUBLESHOOTING_EXTERNAL_DEVICES.md](TROUBLESHOOTING_EXTERNAL_DEVICES.md)**
   - Common issues & solutions
   - Platform-specific fixes
   - Debug information
   - Getting help

3. **[IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)**
   - Technical architecture
   - API endpoints
   - Code structure
   - For developers

---

## 🎮 Interactive Quick Start

Run the interactive guide:

**Windows:**
```
python quick_start_external_devices.py
```

**Mac/Linux:**
```
python3 quick_start_external_devices.py
```

Options:
1. Run FaceVault with external devices
2. Scan for connected devices
3. View documentation
4. Check Python environment
5. Exit

---

## ✨ Tips & Tricks

### Tip 1: Large Device Scans
For devices with 10,000+ photos:
- Create subfolder with recent photos only
- Scan that subfolder first
- Faster than scanning entire device

### Tip 2: USB 3.0 Speed
- USB 3.0 is 10x faster than USB 2.0
- Use USB 3.0 devices if possible
- USB 3.0 ports are typically blue inside

### Tip 3: Space Management
- Check device has ≥100MB free before operations
- Large photo libraries: External HDD recommended
- USB drives: OK for 1000-2000 photos

### Tip 4: Multiple Devices
- Can scan from several devices in one session
- All data consolidates into single database
- Then sort everything to archive drive

### Tip 5: Backup Strategy
```
Photo source (phone)
    ↓
Scan & Organize (FaceVault)
    ↓
Backup #1: USB Drive
Backup #2: External HDD
Backup #3: Online (optional, your choice)
```

---

## 🆘 Need Help?

### Check These First
1. Is device plugged in and recognized by computer?
2. Does device appear in File Explorer/Finder/File Manager?
3. Do you have read permissions to device contents?
4. Is FaceVault server running (see http://localhost:5050)?

### Get More Help
1. Read troubleshooting guide: `TROUBLESHOOTING_EXTERNAL_DEVICES.md`
2. Run quick-start script: `python quick_start_external_devices.py`
3. Check browser console for errors: Press F12 → Console tab
4. Verify device at OS level first (File Manager)

---

## 🎓 What Happens Behind the Scenes

### When You Scan From Device
```
Device (USB, phone, etc)
    ↓
FaceVault reads all photos
    ↓
Face recognition AI detects faces
    ↓
Groups similar faces together (clusters)
    ↓
Stores in local database
    ↓
Photos stored at original path
```

### When You Sort To Device
```
Local database (organized faces)
    ↓
Creates folder structure on device
    ↓
Copies each photo to: Device:/PersonName/0001.jpg
    ↓
Creates "Things Images/" for no-face photos
    ↓
Done! Device now has organized photos
```

---

## ✅ Verification Checklist

After connecting device, verify:
- [ ] Device appears in file manager
- [ ] You can browse files on device
- [ ] At least 100MB free space
- [ ] FaceVault can see the device (modal)
- [ ] Device shows correct type icon (📱 💿 etc)
- [ ] Green checkmark = accessible

---

**Ready to organize? 🚀 Click "🔍 Scan Devices" to get started!**

---

*FaceVault — Organize your memories locally, privately, forever.*
