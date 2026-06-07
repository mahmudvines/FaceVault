# 🔧 Manual External Device Path Entry - Quick Guide

## Problem Solved ✅

If your external hard drive (or any external device) doesn't appear in the **Auto-Detect** list, you can now **manually enter the path** and FaceVault will scan/sort from it!

---

## 🚀 How to Use Manual Path Entry

### Step 1: Find Your Device Path

Your external hard drive needs a path. Find it using your file manager:

**Windows:**
- Open File Explorer
- Look for your external drive (usually shows as a drive letter)
- Examples: `D:\`, `E:\`, `F:\`
- Example with folder: `D:\Photos` or `E:\DCIM`

**macOS:**
- Open Finder
- Look in the sidebar under "Devices"
- Click your external drive
- In the address bar (top), you'll see the path
- Examples: `/Volumes/External_Drive`, `/Volumes/My_Backup`

**Linux:**
- Open File Manager
- Usually mounted in `/media/username/device_name`
- Examples: `/media/user/external_hdd`, `/mnt/usb_drive`

### Step 2: Enter Path in FaceVault

In the **💾 External Devices** section (left sidebar):

1. Click in the text field labeled **"📂 External Device Path"**
2. Paste or type your device path:
   ```
   D:\                    (Windows - whole drive)
   D:\DCIM                (Windows - specific folder)
   /Volumes/MyDrive       (Mac)
   /media/user/external   (Linux)
   ```
3. Click either:
   - **🔍 Scan External** — Scan photos from device
   - **💾 Sort to Path** — Save organized photos to device

---

## 📝 Examples by Platform

### Windows
```
Entire drive:    D:\
With folder:     D:\DCIM
Camera folder:   D:\Pictures
Backup folder:   E:\FaceVault_Backup
```

### macOS
```
External HD:     /Volumes/External_Drive
USB key:         /Volumes/USB_DRIVE
Time Machine:    /Volumes/Time_Machine
```

### Linux
```
USB drive:       /media/user/usb_drive
External HD:     /mnt/external_hdd
External mount:  /media/username/DEVICE_NAME
```

---

## 🎯 Common Scenarios

### Scenario 1: External HDD Connected But Not Detected
```
1. Open File Manager
2. Find external HDD → note the path (e.g., D:\)
3. In FaceVault, paste path in "External Device Path" field
4. Click "🔍 Scan External"
5. Done! ✓
```

### Scenario 2: External Drive with Photos in Subfolder
```
External drive contains: E:\Photos\Vacation\2024\
1. Paste: E:\Photos\Vacation\2024
2. Click "🔍 Scan External"
3. Only photos from that folder are scanned
```

### Scenario 3: Multiple External Drives
```
Drive 1: D:\Old_Photos
  → Click "🔍 Scan External"
  → Result: 500 photos analyzed

Drive 2: E:\Recent_Photos
  → Change path to: E:\Recent_Photos
  → Click "🔍 Scan External"
  → Result: 300 more photos analyzed
  
Total: 800 photos organized!
```

---

## ⚠️ Important Notes

### Path Format
- Windows: Use backslash `\` or forward slash `/`
  - ✅ `D:\DCIM` or `D:/DCIM` (both work)
  - ❌ Don't use `D:` alone without backslash

- Mac/Linux: Always use forward slash `/`
  - ✅ `/Volumes/External_Drive`
  - ❌ Don't use backslashes

### Spaces in Path Names
If your path has spaces, that's fine:
```
✅ /Volumes/My External Drive
✅ D:\Photos and Videos
✅ /media/user/My USB Drive
```

### Case Sensitive (Linux Only)
On Linux, paths are case-sensitive:
```
✅ /media/user/USB_DRIVE (if that's the exact name)
❌ /media/user/usb_drive (won't work if named "USB_DRIVE")
```

---

## ✅ Verification Checklist

Before scanning, verify:
1. [ ] Device is plugged in and visible in File Manager
2. [ ] You copied the correct path
3. [ ] Path exists (try opening it in File Manager)
4. [ ] You can see files in that folder
5. [ ] Device has at least 100MB free space

---

## 🛠️ Troubleshooting Manual Path

### "Invalid device path" Error
- Check path is correct (copy-paste from File Manager)
- Make sure device is connected
- Try removing trailing slash: `D:\` → `D:`

### "No images found"
- Path may not have photos in top level
- Try adding subfolder: `D:\DCIM` or `D:\Pictures`
- Check with File Manager first (open path manually)

### "Permission denied" Error
1. **Windows**: Run FaceVault as Administrator
2. **Mac/Linux**: Check folder permissions
   ```bash
   chmod 755 /path/to/device
   ```

### Path Looks Wrong
- Copy path directly from File Manager address bar
- Don't type manually (easy to make typos)
- Example: Click address bar → Ctrl+C → Ctrl+V in FaceVault

---

## 💡 Pro Tips

### Tip 1: Copy-Paste Path
1. Open File Manager
2. Navigate to your external device
3. Click address bar (top) → Ctrl+A → Ctrl+C
4. Go to FaceVault
5. Click path field → Ctrl+V
6. Done!

### Tip 2: Save Paths You Use Often
Keep a list of your common external drive paths:
```
External HDD:  D:\Backup
USB Drive:     E:\Photos
Camera SD:     F:\DCIM
Laptop Backup: /Volumes/Time_Machine
```

### Tip 3: Batch Scanning
```
Scan path 1 → Wait to complete
Scan path 2 → Wait to complete
Scan path 3 → Wait to complete
→ All organized into one database!
```

### Tip 4: Test Path First
If unsure, open the path in File Manager first to make sure it works:
1. Open File Manager
2. Paste path into address bar
3. Press Enter
4. If it opens → path is correct
5. Now use in FaceVault

---

## 🎯 Workflow with Manual Path Entry

```
External HDD Connected
        ↓
Open File Manager → Find path
        ↓
Paste path in FaceVault
        ↓
Click "🔍 Scan External"
        ↓
FaceVault analyzes all photos
        ↓
Name people in web UI
        ↓
Click "💾 Sort to Path"
        ↓
Organized photos saved to external drive!
```

---

## ✨ You Now Have TWO Ways to Scan External Devices

### Option 1: Auto-Detect
```
💾 External Devices
└── 🔍 Auto-Detect Devices (button)
    ↓ Shows connected devices
    └── Click device → Click "Scan" or "Sort"
```
**Best for**: Devices that are auto-detected

### Option 2: Manual Path Entry
```
💾 External Devices
└── 📂 External Device Path (text field)
    ↓ Enter path manually
    ├── Click "🔍 Scan External"
    └── Click "💾 Sort to Path"
```
**Best for**: 
- Devices not auto-detected
- Specific folders on devices
- Network mounts
- Any time auto-detect doesn't work

---

## 🎉 Summary

You can now:
- ✅ Use auto-detect when devices show up
- ✅ Use manual path when they don't
- ✅ Scan external hard drives easily
- ✅ Organize photos to any external location
- ✅ Work with any device (USB, HDD, Network)

**No more "device not found" problems!** 🚀

---

## 📖 Related Documentation

- `README_EXTERNAL_DEVICES.md` — Overview of all external device features
- `TROUBLESHOOTING_EXTERNAL_DEVICES.md` — Common issues and fixes
- `GETTING_STARTED_EXTERNAL_DEVICES.md` — Getting started guide

---

**Happy organizing!** 📸
