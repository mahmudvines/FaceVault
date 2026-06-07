# External Devices Troubleshooting Guide

## 🔍 Devices Not Detected

### Windows
**Problem**: USB drive or SD card not showing up

**Solutions**:
1. **Check Device Manager**
   - Right-click "This PC" → "Manage" → "Device Manager"
   - Look for "Disk Drives" or "USB Storage Devices"
   - If marked with ⚠️ yellow warning, right-click → "Update driver"

2. **Try Different Port**
   - USB 3.0 ports (blue inside) sometimes have compatibility issues
   - Try a USB 2.0 port or different port on computer

3. **Check File Explorer**
   - Open File Explorer
   - Look for the device under "This PC"
   - Note the drive letter (e.g., `D:\`, `E:\`)
   - If you see it in File Explorer but not in FaceVault, manually enter path

4. **Restart Computer**
   - Unplug device
   - Restart Windows
   - Plug device back in
   - Open FaceVault

### macOS
**Problem**: External drive not appearing

**Solutions**:
1. **Check Finder**
   - Open Finder → "Devices" in sidebar
   - Device should appear automatically
   - If not, try: Apple menu → About This Mac → Storage

2. **Verify Mount Point**
   - Open Terminal
   - Run: `ls /Volumes`
   - Should list your device
   - Use path like `/Volumes/DeviceName`

3. **Try Different Cable/Port**
   - Some older USB cables may not work
   - USB 3.0 ports are more reliable

### Linux
**Problem**: Device mounted but not detected by FaceVault

**Solutions**:
1. **Check Mount Points**
   ```bash
   # View all mounted filesystems
   mount | grep -E 'media|mnt'
   
   # Or use lsblk
   lsblk
   ```

2. **Manual Mount**
   ```bash
   # Find device
   lsblk  # Note device name, e.g., sdb1
   
   # Create mount point
   sudo mkdir -p /mnt/usb
   
   # Mount device
   sudo mount /dev/sdb1 /mnt/usb
   
   # Use /mnt/usb in FaceVault
   ```

3. **Check Permissions**
   ```bash
   # View permissions
   ls -l /mnt/usb
   
   # Grant access if needed
   sudo chown -R $USER:$USER /mnt/usb
   ```

---

## 📱 Mobile Device Issues

### Android Phone Not Recognized

1. **Enable USB Debugging**
   - Settings → Developer options → USB Debugging (toggle ON)
   - If "Developer options" not visible:
     - Settings → About phone
     - Tap "Build number" 7 times
     - Developer options now appears in Settings

2. **Change USB Mode**
   - Swipe down from top of screen (notification panel)
   - Tap "USB charging" notification
   - Select "File Transfer" or "MTP (Media Transfer Protocol)"
   - **Not** "Charging only"

3. **Unlock Phone When Connected**
   - Phone must be unlocked for file access
   - FaceVault cannot access locked phones

4. **Trust the Computer**
   - If prompted "Trust this computer?", tap "ALLOW" or "TRUST"

### iPhone Not Detected

1. **Tap "Trust"**
   - Connect iPhone
   - Unlock phone
   - If prompted: "Trust This Computer?" → Tap "Trust"

2. **Check iOS Version**
   - iPhone must have iOS 13 or later
   - Update iPhone if needed

3. **Disable iCloud Drive**
   - Settings → [Your Name] → iCloud
   - Toggle "iCloud Drive" OFF temporarily
   - Try again

4. **Check Files App Access**
   - Settings → Privacy → Files and Folders
   - Ensure access is granted

5. **Try Different Cable**
   - Authentic Apple Lightning cables work best
   - Third-party cables may not support file transfer

---

## ⚠️ Permission Errors

### "No write permissions" Error

**On Windows**:
1. Right-click device in File Explorer
2. Properties → Security tab
3. Click "Edit" → Your username → Check "Full Control"
4. Click "Apply" → "OK"

**Or run FaceVault as Admin**:
1. Find FaceVault launcher
2. Right-click → "Run as administrator"

**On macOS/Linux**:
```bash
# Check permissions
ls -ld /path/to/device

# Grant full permissions
chmod -R 755 /path/to/device

# Or change owner
sudo chown -R $USER /path/to/device
```

### "Access denied" on Device

**Device might be read-only**:
1. Right-click device → Properties
2. Check "Read-only" checkbox
3. If checked, uncheck it

**Or try**:
```bash
# On Mac/Linux
chmod +w /path/to/device
```

---

## 🐢 Slow Performance

### Scanning Very Slow (Taking 30+ minutes)

**Likely causes**:
- USB 2.0 device (slow bus speed)
- Large folder (10,000+ photos)
- Very old computer
- External drive over network connection

**Solutions**:
1. **Use USB 3.0 Hub**
   - USB 3.0 is 10x faster than USB 2.0
   - Invest in USB 3.0 external drive

2. **Reduce Number of Photos**
   - Create subfolder with recent photos
   - Scan one folder at a time

3. **Use Faster Connection**
   - Local USB is faster than network storage
   - SD cards faster if using USB 3.0 reader

4. **Check CPU Usage**
   - Face recognition is CPU-intensive
   - Close other apps
   - Slower computers take longer

---

## 💾 Storage Issues

### "Not enough space" Error

1. **Check Available Space**
   - Device must have at least 100MB free
   - Each photo needs ~5-10MB temporary space

2. **Free Up Space**
   - Delete unnecessary files from device
   - Or sort photos to a different device

3. **Use Larger Device**
   - Upgrade to larger USB drive or hard drive

### Device Full After Sorting

**Reason**: Sorted photos may take more space than source

**Solutions**:
1. Delete source photos if no longer needed
2. Compress photos before sorting
3. Use two devices (source + destination)

---

## 🔗 Connection Issues

### Device Connects Then Disconnects

**Likely causes**:
- Faulty USB cable
- USB port getting loose
- Device driver issue

**Solutions**:
1. **Try Different Cable**
   - Use known-working USB cable
   - Avoid cheap cables

2. **Try Different Port**
   - USB ports can wear out
   - Try another port on computer
   - Try different computer if available

3. **Update Drivers**
   - Windows: Right-click device in Device Manager → Update driver
   - Mac: Usually auto-updated
   - Linux: Run `sudo apt-get update && sudo apt-get upgrade`

4. **Clean USB Connector**
   - Gently clean gold connector on USB device
   - Use soft, dry cloth
   - Avoid water or alcohol

---

## 🖱️ UI/Button Issues

### "Scan Devices" Button Not Working

**Try**:
1. **Refresh Page**
   - Browser: F5 or Ctrl+R
   - Close and reopen browser

2. **Check Server Running**
   - See "http://localhost:5050" in address bar
   - Server should show: "FaceVault is running..."

3. **Check Browser Console**
   - Press F12 (Developer Tools)
   - Click "Console" tab
   - Look for error messages
   - Screenshot and share error

### Device Not Showing in Modal

1. **Rescan Again**
   - Click "Scan Devices" button again
   - Device may need 2-3 seconds to mount

2. **Check Device is Connected**
   - Verify device appears in File Explorer/Finder/File Manager
   - If not there, problem is OS-level

3. **Restart FaceVault**
   - Close FaceVault window
   - Close Terminal running app.py
   - Reconnect device
   - Start FaceVault again

---

## 🚀 Still Having Issues?

### Debug Information to Collect

1. **What's your OS?**
   - Windows 10/11, macOS version, Linux distro

2. **What device?**
   - USB drive, SD card, phone (what model/OS), external HDD

3. **What error message?**
   - Screenshots help a lot
   - Copy exact error text

4. **Server Log**
   - Run FaceVault in Terminal
   - Look for error messages
   - Screenshot the terminal output

### Try These Steps

1. **Restart Everything**
   ```
   Close FaceVault
   Disconnect device
   Wait 10 seconds
   Restart computer
   Reconnect device
   Start FaceVault
   ```

2. **Manually Test Path**
   - In Scan Folder field, enter exact device path
   - Example Windows: `D:\DCIM`
   - Example Mac: `/Volumes/USB_DRIVE`
   - Example Linux: `/media/username/DEVICE`
   - Click "Scan" button

3. **Check with File Manager**
   - Open device in File Explorer/Finder/Nautilus
   - Navigate to photo folder
   - Copy exact path
   - Paste into FaceVault

---

## 📞 Getting Help

If you can't solve it:

1. **Check Documentation**
   - Read: `EXTERNAL_DEVICES_GUIDE.md`
   - Read: `IMPLEMENTATION_NOTES.md`

2. **Test with Command Line**
   ```bash
   # Run quick start utility
   python quick_start_external_devices.py
   
   # Select option 2: Scan Devices
   # See if device is detected at OS level
   ```

3. **Share Information**
   - OS and version
   - Device type and capacity
   - Error message (screenshot)
   - What you were trying to do
   - FaceVault terminal output

---

## ✅ Verification Checklist

Before troubleshooting, verify:

- [ ] Device appears in OS file manager (File Explorer/Finder/Nautilus)
- [ ] Device is readable (you can view files with file manager)
- [ ] Device has photos in standard locations:
      - Windows camera: `D:\DCIM` or `D:\Pictures`
      - Phone: `/DCIM` or `/Pictures`
      - SD card: `/DCIM` or root level photos
- [ ] You have read permissions (can view files)
- [ ] You have write permissions (can create files, if sorting to device)
- [ ] Device has at least 100MB free space
- [ ] FaceVault server is running (see "http://localhost:5050")
- [ ] Browser is on the same machine as FaceVault server

---

**Happy organizing! 📸**
