# 📱 FaceVault External Device Support

> Scan and organize photos from USB drives, SD cards, mobile devices, and external hard drives

## 🎯 Features

### Supported Devices
- 💾 **USB Drives / Pen Drives** — Automatic detection and mounting
- 💿 **SD Cards** — Including microSD cards via USB readers
- 📱 **Mobile Devices** — iOS and Android phones via USB cable
- 🖥 **External Hard Drives** — USB-connected external storage
- 🌐 **Network Storage** — Via local mounts (Windows, macOS, Linux)

### Capabilities
✅ Automatically detect all connected external devices  
✅ Scan images directly from external storage  
✅ Organize detected faces and save sorted photos to external device  
✅ View device space, type, and accessibility status  
✅ No data copying to local machine (optional privacy mode)  
✅ Works across Windows, macOS, and Linux  

---

## 🚀 How to Use

### Step 1: Connect Your Device
- **USB Drive**: Plug into USB port
- **SD Card**: Insert into SD card reader connected via USB
- **Mobile Phone**: Connect via USB cable (enable file transfer mode)
  - **iOS**: Trust the computer when prompted
  - **Android**: Set USB mode to "File Transfer" or "MTP"
- **External Hard Drive**: Connect via USB

### Step 2: Detect Devices in FaceVault

1. Open FaceVault in your browser (`http://localhost:5050`)
2. Click **💾 Scan Devices** in the left sidebar
3. Wait for device detection to complete
4. You'll see all connected devices with:
   - Device type icon (📱 mobile, 💿 SD card, etc.)
   - Device name/label
   - Available space and total capacity
   - Accessibility status

### Step 3: Choose an Action

#### Option A: Scan Images FROM Device
1. Select the device from the list
2. Click **🔍 Scan Selected**
3. FaceVault will:
   - Find all photos on the device
   - Detect faces using AI
   - Group faces by person
   - Add results to your local database

#### Option B: Save Sorted Photos TO Device
1. First, scan and organize your photos (local or external)
2. Name the people you've identified
3. Select an external device
4. Click **💾 Sort to Device**
5. Organized folders will be created:
   ```
   [Device]:
   ├── Person Name 1/
   │   ├── 0001.jpg
   │   ├── 0002.jpg
   │   └── ...
   ├── Person Name 2/
   ├── Things Images/  (photos with no faces)
   └── ...
   ```

---

## 📂 Device Paths

### Windows
- USB drives appear as letters: `D:\`, `E:\`, `F:\`, etc.
- You can type the path directly in the Scan/Sort fields
- Example: `D:\DCIM` (common camera folder on SD cards)

### macOS
- Devices mount in `/Volumes/`
- Example: `/Volumes/USB_DRIVE/Pictures`
- Example: `/Volumes/iPhone/DCIM`

### Linux
- USB drives typically mount in `/media/username/` or `/mnt/`
- Example: `/media/user/USB_DRIVE/photos`

---

## 🎮 Using the Web Interface

### "Scan Devices" Button
Located in **💾 External Devices** section:
- Detects all removable drives
- Shows device type, space, and status
- Click a device to select it

### Direct Path Entry
You can also manually enter a device path:
```
[Scan Folder field]:  D:\DCIM
→ Click "Scan"
```

```
[Output Path field]:  E:\FaceVault_Organized
→ Click "Sort"
```

---

## 🔧 Advanced Usage

### Find Images on Connected Device
Click the device in the modal to see:
- Total images found
- Image paths
- Available storage space

### Copy Organized Photos to Device
1. Organize your local photos first
2. Select destination device
3. Click **💾 Sort to Device**
4. Photos are **copied** to external storage (originals remain on your computer)

### Create Database on External Device
You can keep your face recognition database on an external drive:
1. Copy `facevault_db.json` to your external device
2. Modify paths in future scans to reference the device

---

## ⚙️ Technical Details

### Supported Formats
Images: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`

### Device Detection
- **Windows**: Scans drive letters C-Z and checks drive type (removable, external fixed)
- **macOS**: Checks `/Volumes` directory for non-system drives
- **Linux**: Checks `/media` and `/mnt` directories

### Permissions
- Requires **read access** to scan images from device
- Requires **write access** to save sorted photos to device
- Windows may prompt for admin on some external drives
- macOS/Linux: Ensure your user has access to mounted volumes

---

## 🛠 Troubleshooting

### Device Not Appearing
1. **Check connection**: Unplug and reconnect the device
2. **Try different USB port**: Some ports may have issues
3. **Restart app**: Close and reopen FaceVault
4. **Wait for mount**: Some devices take 2-3 seconds to mount

### "No write permissions" Error
- Windows: Right-click FaceVault launcher → "Run as Administrator"
- macOS/Linux: Check file permissions on the external drive
- Try a different USB port or cable

### Mobile Phone Not Detected
- **Android**: Unlock phone, swipe down notification panel, check USB mode is "File Transfer"
- **iOS**: Tap "Trust" on the "Trust This Computer?" prompt
- Try: `iphone usb file access` or Android file transfer app

### Slow Scanning
- External USB 2.0 drives are slower than USB 3.0
- Use a USB 3.0 hub for multiple devices
- Scanning 10,000+ photos may take 10-30 minutes

### Photos Not Showing
- Device may not have images in common locations
- Try specific folders: `/DCIM`, `/Photos`, `/Pictures`
- Check file permissions

---

## 🔒 Privacy Notes

✅ **100% Local** — No data is sent to the cloud  
✅ **Optional Copying** — You decide if photos are copied or accessed in-place  
✅ **No Internet Required** — Works offline completely  
✅ **On External Storage** — Keep all data on your external device if desired  

---

## 📊 Example Workflows

### Workflow 1: Mobile Phone → Organize → USB Drive
```
1. Connect iPhone/Android → Click "Scan Devices"
2. Select phone → Click "🔍 Scan Selected"
3. FaceVault detects all faces and groups them
4. Name the people in the web UI
5. Connect USB drive → Click "💾 Sort to Device"
6. Organized photos saved to USB drive
```

### Workflow 2: Multi-Device Consolidation
```
1. Connect SD Card → Scan → Find 500 photos
2. Connect USB Drive → Scan → Find 300 photos
3. Connect Mobile → Scan → Find 200 photos
→ Total: 1000 photos, 45 people identified
4. Connect External HDD → Sort all photos there
→ Now have organized backup on external hard drive
```

### Workflow 3: Family Photo Archival
```
1. Scan all devices: cameras, phones, old hard drive
2. Consolidate 10,000+ family photos
3. AI groups by person (grandkids, parents, etc.)
4. Manually verify and name groups
5. Save to external archive drive with organization
```

---

## 🐛 Known Limitations

- Cannot directly modify photos on device (copies to device, doesn't modify source)
- Very large external drives (100GB+) may take time to index
- Some old USB 2.0 devices may require longer timeouts
- Network shares must be locally mounted to appear

---

## 📞 Support

- Check device is properly connected and recognized by OS
- Verify you have read/write permissions
- Try connecting to different USB ports
- Restart FaceVault and reconnect device
- Check storage space (device must have >100MB free)

---

**Made with ❤️ for organizing your memories.**
