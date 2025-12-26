# Open Textile Intelligence - Desktop Application

## Native Desktop Application for Windows

This is a **real native desktop application** built with PySide6 (Qt for Python), NOT a web application.

## Features

- **Native Windows Application**: Opens as a native window, no browser required
- **Real-Time Detection**: Live updates with smooth animations
- **Dark Industrial Theme**: Professional monitoring interface
- **Thread-Safe**: Background detection doesn't block UI
- **PyInstaller Ready**: Can be packaged as standalone .exe

## Installation

### 1. Install Dependencies

```bash
cd Open-Textile-Intelligence
pip install -r requirements.txt
```

Required packages:
- `PySide6` - Qt framework for Python
- `rich` - Terminal output (optional)
- `numpy` - Numerical operations

### 2. Run the Application

```bash
cd desktop_app
python main.py
```

The application window will open immediately.

## Usage

1. **Adjust Scan Duration**: Use the slider (5-60 seconds)
2. **Start Scan**: Click "▶ Taramayı Başlat"
3. **Watch Real-Time Detection**: Defects appear in the table as they're detected
4. **Stop Anytime**: Click "⏹ Durdur" to stop early

## Interface Components

### Top Metrics
- **📏 Taranan Uzunluk**: Total scanned length in yards
- **⚠️ Tespit Edilen Kusur**: Number of defects detected
- **✅ Verimlilik Oranı**: Efficiency percentage
- **🔄 Durum**: Current system status

### Progress Bars
- **Sensör Kalibrasyonu**: Sensor calibration progress
- **Kumaş Tarama İlerlemesi**: Fabric scanning progress

### Detection Table
Live stream of detected defects with:
- Timestamp
- Frame ID
- Status indicator
- Defect type (color-coded by severity)
- Confidence percentage

### Color Coding
- 🔴 **Red**: Critical defects (Delik, İplik Kopması)
- 🟡 **Yellow**: Warnings (Renk Uyuşmazlığı)
- 🟠 **Orange**: Medium issues (Leke, Dokuma Hatası)

## Architecture

```
desktop_app/
├── main.py                    # Entry point
├── detection_manager.py       # Background detection thread
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # Main window class
│   └── styles.py              # Dark theme styling
└── README.md                  # This file
```

### Thread Architecture

```
Main Thread (UI)
    ↓
    Signals/Slots
    ↓
Background Thread (DetectionManager)
    ↓
    FabricScanner (Detection Logic)
```

## Packaging as .exe

### Using PyInstaller

```bash
pip install pyinstaller

# Simple packaging
pyinstaller --onefile --windowed --name="OpenTextileIntelligence" main.py

# Advanced with icon
pyinstaller --onefile --windowed --icon=icon.ico --name="OpenTextileIntelligence" main.py
```

Output: `dist/OpenTextileIntelligence.exe`

### Distribution

The generated .exe can be distributed standalone on Windows machines without Python installation.

## Technical Details

### UI Framework
- **PySide6**: Official Qt bindings for Python
- **QMainWindow**: Main application window
- **QTableWidget**: Detection table
- **QProgressBar**: Progress indicators
- **QThread**: Background processing

### Real-Time Updates
- Detection runs in separate thread (DetectionManager)
- Qt Signals communicate with UI thread
- New rows animate with brief highlight
- Automatic scrolling to latest detection

### Styling
- Custom dark theme with industrial aesthetic
- Gradient metric cards
- Color-coded defect severity
- High contrast for readability

## Comparison: Web vs Desktop

| Feature | Web (Streamlit) | Desktop (PySide6) |
|---------|----------------|-------------------|
| Type | Browser-based | Native window |
| Performance | Good | Excellent |
| Offline | No | Yes |
| .exe Packaging | No | Yes |
| System Integration | Limited | Full |
| Startup Time | Slower | Fast |

## Development

### Adding New Features

1. **UI Changes**: Edit `ui/main_window.py`
2. **Styling**: Modify `ui/styles.py`
3. **Detection Logic**: Update `detection_manager.py`
4. **Entry Point**: Configure `main.py`

### Debugging

Run with console output:
```bash
python main.py
```

Check terminal for any error messages.

## Future Enhancements

- [ ] Export detection report to PDF
- [ ] Save/load scan sessions
- [ ] Real camera feed integration
- [ ] Multi-language support
- [ ] System tray integration
- [ ] Auto-update mechanism

## License

MIT License - See main project LICENSE file

## Author

**Bahattin Yunus Çetin**
IT Architect
Trabzon, Turkey

---

**This is a native desktop application. No web server or browser required.**
