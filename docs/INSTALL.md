# Installation Guide - Open Textile Intelligence

## System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Python**: 3.9 or higher
- **RAM**: Minimum 8GB (16GB recommended for ML)
- **Camera**: USB webcam or integrated camera
- **Display**: 1920x1080 or higher recommended

---

## Step 1: Install Python

1. Download Python 3.9+ from https://www.python.org/downloads/
2. During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

---

## Step 2: Install Dependencies

### Option A: Full Installation (ML + Camera Support)

Open Command Prompt as Administrator and run:

```cmd
cd C:\Users\yunus\Desktop\Projects\Open-Textile-Intelligence
pip install -r requirements.txt
```

This will install:
- PySide6 (Qt GUI framework)
- OpenCV (Camera support)
- PyTorch (Machine Learning)
- TorchVision (Computer Vision models)
- NumPy (Numerical computing)
- Pillow (Image processing)

### Option B: CPU-Only PyTorch (Recommended for Most Users)

If you don't have an NVIDIA GPU or want faster installation:

```cmd
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install PySide6 opencv-python numpy pillow rich
```

### Option C: GPU-Accelerated PyTorch (For NVIDIA GPUs)

If you have an NVIDIA GPU and want faster ML inference:

1. Check your CUDA version:
   ```cmd
   nvidia-smi
   ```

2. Install PyTorch with CUDA support:
   ```cmd
   # For CUDA 11.8
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

   # For CUDA 12.1
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

3. Install other dependencies:
   ```cmd
   pip install PySide6 opencv-python numpy pillow rich
   ```

For more PyTorch installation options, visit: https://pytorch.org/get-started/locally/

---

## Step 3: Configure Camera Permissions (Windows)

### Windows 10/11 Privacy Settings

1. Open **Settings** (Windows + I)
2. Go to **Privacy & Security** → **Camera**
3. Enable:
   - ✅ "Let apps access your camera"
   - ✅ "Let desktop apps access your camera"

### Verify Camera Access

Run the test script:
```cmd
cd C:\Users\yunus\Desktop\Projects\Open-Textile-Intelligence
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAILED'); cap.release()"
```

Expected output: `Camera OK`

---

## Step 4: Run the Application

### Launch the Desktop App

```cmd
cd C:\Users\yunus\Desktop\Projects\Open-Textile-Intelligence
python desktop_app/main.py
```

Or use the batch file:
```cmd
run_desktop.bat
```

---

## Troubleshooting

### Error: "No module named 'torch'"

**Solution**: Install PyTorch
```cmd
pip install torch torchvision
```

### Error: "Camera access denied"

**Solutions**:
1. Check Windows Privacy Settings (see Step 3)
2. Close other camera apps (Zoom, Teams, Skype)
3. Reconnect USB camera
4. Try different USB port
5. Update camera drivers

### Error: "No module named 'cv2'"

**Solution**: Install OpenCV
```cmd
pip install opencv-python
```

### Error: "No module named 'PySide6'"

**Solution**: Install PySide6
```cmd
pip install PySide6
```

### Application crashes on startup

**Solutions**:
1. Update graphics drivers
2. Run in compatibility mode (Windows 10)
3. Check Python version (must be 3.9+)
4. Reinstall dependencies:
   ```cmd
   pip uninstall -y torch torchvision PySide6 opencv-python
   pip install -r requirements.txt
   ```

### Camera shows black screen

**Solutions**:
1. Test camera in Windows Camera app
2. Check if other apps are using camera
3. Restart computer
4. Update webcam driver from Device Manager

### ML models fail to load

**Solutions**:
1. Check internet connection (first run downloads pretrained weights)
2. Clear PyTorch cache:
   ```cmd
   rmdir /s /q %USERPROFILE%\.cache\torch
   ```
3. Reinstall PyTorch:
   ```cmd
   pip uninstall torch torchvision
   pip install torch torchvision
   ```

---

## Verification Checklist

After installation, verify each component:

### ✅ Python & Dependencies
```cmd
python -c "import PySide6; print('PySide6 OK')"
python -c "import cv2; print('OpenCV OK')"
python -c "import torch; print('PyTorch OK')"
python -c "import torchvision; print('TorchVision OK')"
```

### ✅ Camera Access
```cmd
python desktop_app/test_camera.py
```

### ✅ ML Pipeline
```cmd
cd desktop_app
python -c "from ml.pipeline import create_ml_pipeline; print('ML Pipeline OK')"
```

---

## Performance Optimization

### For Better ML Inference Speed:

1. **Use GPU** (if available):
   - Install CUDA-enabled PyTorch
   - Verify GPU usage: Application will show "CUDA" in status

2. **Reduce Image Resolution**:
   - Camera feeds are resized to 224x224 for ML
   - Larger feeds don't improve accuracy

3. **Adjust Confidence Threshold**:
   - Edit `desktop_app/ui/main_window.py` line 469
   - Lower = more detections (more false positives)
   - Higher = fewer detections (more false negatives)

---

## Updating the Application

```cmd
cd C:\Users\yunus\Desktop\Projects\Open-Textile-Intelligence
git pull
pip install -r requirements.txt --upgrade
```

---

## Getting Help

- **Issues**: https://github.com/anthropics/open-textile-intelligence/issues
- **Documentation**: See README.md
- **ML Details**: See ML_SYSTEM_DOCUMENTATION.md

---

## License

This project uses:
- PySide6 (LGPL)
- PyTorch (BSD-3-Clause)
- OpenCV (Apache 2.0)

See individual package licenses for details.
