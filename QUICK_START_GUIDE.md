# 🚀 Quick Start Guide - Open Textile Intelligence

## ✅ What Was Fixed

**Camera Access:**
- ✅ Camera now opens correctly with proper permission checking
- ✅ Clear error messages when camera blocked
- ✅ Windows privacy settings instructions shown
- ✅ Test camera button added

**UI Layout:**
- ✅ Window fits 1920x1080 screens perfectly
- ✅ Responsive layout - no cut-off elements
- ✅ Automatic window centering
- ✅ Dynamic sizing based on screen resolution

---

## 🎯 How to Run

```bash
cd Open-Textile-Intelligence
python desktop_app/main.py
```

---

## 📷 Testing Your Camera

### Step 1: Test Camera Access

1. Launch the application
2. Click **"📷 Kamerayı Test Et"** button
3. Wait for result dialog

**If Successful:**
- ✅ Dialog shows: "Kamera erişimi başarılı!"
- You're ready to use camera mode

**If Failed:**
- ❌ Dialog shows detailed error with Windows instructions
- Follow the steps shown in the dialog:

```
WINDOWS KAMERA İZİNLERİNİ AÇMAK İÇİN:
1. Windows Ayarlar'ı açın (Win + I)
2. Gizlilik ve Güvenlik → Kamera
3. 'Uygulamaların kameraya erişmesine izin ver' → AÇIK
4. Uygulamayı yeniden başlatın
```

---

## 🎬 Using Camera Mode

### Option 1: Simulation Mode (Default)
1. Mode is already set to **"SİMÜLASYON MODU"**
2. Click **"▶ Taramayı Başlat"**
3. Watch artificial defects being generated

### Option 2: Real Camera Mode
1. Click mode selector dropdown
2. Select **"GERÇEK KAMERA MODU – Canlı Giriş"**
3. Click **"▶ Taramayı Başlat"**
4. Watch for camera status:
   - "Kamera Açılıyor..." → Camera initializing
   - "✅ Kamera Aktif – Canlı Görüntü" → Success!
   - Live video appears in left panel
   - FPS counter updates in real-time

---

## ⚠️ Troubleshooting

### Problem: "Kamera açılamadı"

**Possible Causes:**
1. Camera not plugged in
2. Windows privacy settings blocking camera
3. Another app using camera (Zoom, Teams, etc.)

**Solutions:**
1. Check USB cable connection
2. Enable camera in Windows Settings:
   - Press Win + I
   - Go to: Privacy & Security → Camera
   - Turn ON: "Let apps access your camera"
3. Close other apps using camera
4. Restart application

### Problem: "Kare okunamadı"

**Possible Causes:**
1. USB connection unstable
2. Camera driver issue

**Solutions:**
1. Unplug and replug camera
2. Try different USB port
3. Restart computer

### Problem: UI Elements Cut Off

**Solution:**
- This should be fixed! Window auto-sizes to screen
- If still an issue, manually resize window
- Window should fit on 1920x1080 and smaller screens

---

## 🎮 UI Features

### New Elements

**1. Camera Test Button**
- Location: Top control panel
- Label: "📷 Kamerayı Test Et"
- Function: Pre-flight camera check
- Shows success/error dialog

**2. Camera Status Label**
- Location: Above camera view
- Shows:
  - "Kamera Kapalı – Tarama başlatılmadı"
  - "Kamera Açılıyor..."
  - "✅ Kamera Aktif – Canlı Görüntü"
  - "❌ Kamera Erişim Hatası"

**3. Camera Warning Badge**
- Location: Next to mode selector
- Label: "⚠️ Kamera erişimi engellendi"
- Appears: When camera permission denied
- Hidden: When camera works

### Existing Elements (Unchanged)

- Mode selector dropdown
- Start/Stop buttons
- Duration slider
- Metric cards
- Progress bars
- Detection table
- FPS counter

---

## 📊 Visual Status Indicators

| Indicator | Color | Meaning |
|-----------|-------|---------|
| **Mode: SİMÜLASYON** | 🟠 Orange | Simulation mode active |
| **Mode: GERÇEK KAMERA** | 🟢 Green | Camera mode active |
| **Camera Status: Kapalı** | ⚫ Gray | Camera not active |
| **Camera Status: Açılıyor** | 🟠 Orange | Camera initializing |
| **Camera Status: Aktif** | 🟢 Green | Camera working |
| **Camera Status: Hata** | 🔴 Red | Camera failed |
| **Warning Badge** | 🔴 Red | Permission denied |

---

## 💡 Best Practices

### Before Starting

1. **Always test camera first:**
   - Click "📷 Kamerayı Test Et"
   - Verify success before scanning

2. **Close other camera apps:**
   - Zoom, Teams, Skype
   - Browser tabs using camera
   - Windows Camera app

3. **Check Windows permissions:**
   - Windows Settings → Camera
   - Verify "Allow apps" is ON

### During Scanning

1. **Monitor camera status label:**
   - Should show "✅ Kamera Aktif"
   - Live video should be visible
   - FPS should update (25-30)

2. **Don't switch modes during scan:**
   - Mode selector is locked
   - Stop scan first, then switch

3. **Watch for errors:**
   - Error dialogs show immediately
   - Camera view shows error text
   - Warning badge appears

---

## 🔄 Typical Workflow

### First Time Use

```
1. Launch: python desktop_app/main.py
   ↓
2. Click: "📷 Kamerayı Test Et"
   ↓
3a. Success → Go to step 4
3b. Failure → Fix Windows permissions → Retry step 2
   ↓
4. Select: "GERÇEK KAMERA MODU"
   ↓
5. Click: "▶ Taramayı Başlat"
   ↓
6. Verify: Camera status = "✅ Kamera Aktif"
   ↓
7. Watch: Live video + detections
```

### Subsequent Use

```
1. Launch: python desktop_app/main.py
   ↓
2. Select mode: Simulation or Camera
   ↓
3. Click: "▶ Taramayı Başlat"
   ↓
4. Monitor results
```

---

## ⌨️ Keyboard Shortcuts

Currently none implemented. Use mouse/touchpad for all interactions.

---

## 📏 Window Sizing

**Automatic:**
- Window resizes to 95% of screen size
- Maximum: 1800 x 950 pixels
- Centered on screen
- Works on screens ≥ 1366x768

**Manual:**
- Drag edges to resize
- Camera view and table resize proportionally
- No scroll bars needed (responsive layout)

---

## 🆘 Emergency Troubleshooting

### Application Won't Start

```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Run directly
cd desktop_app
python main.py
```

### Camera ALWAYS Fails

1. Test in Windows Camera app first
2. Update camera drivers
3. Try different camera (if available)
4. Check Device Manager for camera device
5. Restart Windows

### UI Looks Wrong

1. Update PySide6:
   ```bash
   pip install --upgrade PySide6
   ```
2. Clear any cached files
3. Restart application

---

## 📞 Support

If issues persist:

1. Check camera in other apps (Windows Camera, Zoom)
2. Review Windows Event Viewer for errors
3. Try different USB port/camera
4. Verify OpenCV installation:
   ```python
   import cv2
   print(cv2.__version__)
   cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
   print("Opened:", cap.isOpened())
   cap.release()
   ```

---

## ✅ Success Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Camera works in Windows Camera app
- [ ] Windows camera permissions enabled
- [ ] No other apps using camera
- [ ] Camera test button shows success
- [ ] USB connection stable

---

**Application is production-ready with comprehensive camera permission handling and responsive UI.**

**Last Updated:** 2025-12-26
**Version:** 1.0
