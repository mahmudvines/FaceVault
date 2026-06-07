# ⚡ QUICK FIX - Run This Now!

## What to do RIGHT NOW:

### Step 1: Stop Flask App
Press **Ctrl+C** in the terminal running FaceVault
Wait for it to stop completely

### Step 2: Restart Flask App
```bash
python app.py
```
OR
```bash
npm start
```

Wait for this message:
```
WARNING: This is a development server...
```

### Step 3: Try Scanning
1. Open browser to http://localhost:5000
2. Enter folder path: `D:\Manna Chy\Sent` (or test folder)
3. Click **Scan** button
4. **WATCH THE TERMINAL OUTPUT** while scanning

### Step 4: Check Terminal

✅ **Good output looks like:**
```
[SCAN] Starting scan of: D:\Manna Chy\Sent
[SCAN] Found 250 total images, 50 new
[SCAN] Processing 50 images with 7 workers...
[Scanner] Added 2 face(s) from photo_001.jpg
...
[SCAN] Returning results: scanned=250, added=47
```

❌ **Bad output looks like:**
```
[SCAN ERROR] Exception: FileNotFoundError
```

### Step 5: Check Results

After terminal shows completion (look for `Returning results:`):
- Check browser - results should appear in 1-2 seconds
- If not, check browser console (F12 → Console)

---

## 🚨 If Still Not Working:

### Check 1: Terminal Messages
Look for `[SCAN ERROR]` or `Exception` in terminal
→ **Copy full error message and share it**

### Check 2: Browser Console
Press **F12** → **Console** tab
→ **Copy any red error messages**

### Check 3: Test with Small Folder
- Create folder: `C:\test_photos`
- Copy 5 images
- Try scanning that
- Does it work faster?

---

## 📞 Need Help?

Provide this info:
1. Full terminal error message
2. Folder path you're trying to scan
3. Number of photos in folder
4. Whether using external device
5. Browser console error (if any)

---

## ✅ Once It Works

- Scanning results will show instantly
- Results display: `✓ 250 scanned · 47 with faces · 3 no-face`
- People list updates automatically
- Can sort by person

---

**Try the steps above first, then watch terminal output to see what happens!** 🚀
