"""
Windows 11 Modern Dark Theme for Open Textile Intelligence.
Clean, minimal, professional design with proper spacing and typography.
"""

# Windows 11 inspired modern dark theme
DARK_THEME = """
QMainWindow {
    background-color: #202020;
}

QWidget {
    background-color: #202020;
    color: #ffffff;
    font-family: 'Segoe UI', 'Segoe UI Variable', 'Arial', sans-serif;
    font-size: 10pt;
}

/* Metric Cards - Windows 11 Style */
QFrame#metricCard {
    background-color: #2b2b2b;
    border-radius: 12px;
    border: 1px solid #3a3a3a;
    padding: 0px;
    margin: 0px;
}

QFrame#metricCard:hover {
    background-color: #303030;
    border: 1px solid #404040;
}

QLabel#metricTitle {
    color: #a0a0a0;
    font-size: 9pt;
    font-weight: 600;
    padding: 0px;
    margin: 0px;
}

QLabel#metricValue {
    color: #ffffff;
    font-size: 32pt;
    font-weight: 600;
    padding: 0px;
    margin: 0px;
}

QLabel#metricUnit {
    color: #909090;
    font-size: 11pt;
    font-weight: 400;
    padding: 0px;
    margin: 0px;
}

/* Table - Modern flat design */
QTableWidget {
    background-color: #2b2b2b;
    alternate-background-color: #282828;
    color: #ffffff;
    gridline-color: #3a3a3a;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    selection-background-color: #0067c0;
}

QTableWidget::item {
    padding: 12px 16px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #0067c0;
    color: white;
}

QHeaderView::section {
    background-color: #252525;
    color: #ffffff;
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid #3a3a3a;
    font-weight: 600;
    font-size: 10pt;
}

/* Progress Bars - Windows 11 style */
QProgressBar {
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    text-align: center;
    background-color: #2b2b2b;
    color: #ffffff;
    height: 28px;
    font-size: 9pt;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #0067c0;
    border-radius: 5px;
}

QProgressBar#calibrationBar::chunk {
    background-color: #0f7b0f;
}

QProgressBar#scanningBar::chunk {
    background-color: #0067c0;
}

/* Section Labels */
QLabel#sectionTitle {
    color: #ffffff;
    font-size: 14pt;
    font-weight: 600;
    padding: 8px 0px;
}

QLabel#statusLabel {
    color: #a0a0a0;
    font-size: 9pt;
    padding: 6px 12px;
    background-color: #2b2b2b;
    border-radius: 6px;
}

/* Buttons - Windows 11 Accent Style */
QPushButton {
    background-color: #0067c0;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 10pt;
    font-weight: 600;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #005ba1;
}

QPushButton:pressed {
    background-color: #004a7f;
}

QPushButton:disabled {
    background-color: #3a3a3a;
    color: #707070;
}

QPushButton#startButton {
    background-color: #0f7b0f;
}

QPushButton#startButton:hover {
    background-color: #0d6b0d;
}

QPushButton#startButton:pressed {
    background-color: #0a5a0a;
}

QPushButton#stopButton {
    background-color: #d13438;
}

QPushButton#stopButton:hover {
    background-color: #b52e31;
}

QPushButton#stopButton:pressed {
    background-color: #9a272a;
}

QPushButton#testCameraButton {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #3a3a3a;
}

QPushButton#testCameraButton:hover {
    background-color: #353535;
}

/* Combo Box - Modern dropdown */
QComboBox {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 10pt;
    min-height: 32px;
}

QComboBox:hover {
    border: 1px solid #505050;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #a0a0a0;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    selection-background-color: #0067c0;
    padding: 4px;
}

/* Slider - Modern minimal */
QSlider::groove:horizontal {
    background: #2b2b2b;
    height: 6px;
    border-radius: 3px;
    border: 1px solid #3a3a3a;
}

QSlider::handle:horizontal {
    background: #0067c0;
    width: 18px;
    height: 18px;
    margin: -7px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #005ba1;
}

/* Scrollbar - Minimal modern design */
QScrollBar:vertical {
    background-color: #202020;
    width: 12px;
    border: none;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #505050;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #606060;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* Status Bar */
QStatusBar {
    background-color: #252525;
    color: #ffffff;
    border-top: 1px solid #3a3a3a;
    font-size: 9pt;
}

/* Splitter */
QSplitter::handle {
    background-color: #3a3a3a;
}

QSplitter::handle:hover {
    background-color: #505050;
}
"""

# Color codes for defect severity (Windows 11 semantic colors)
DEFECT_COLORS = {
    "Delik": "#d13438",              # Critical - Red
    "İplik Kopması": "#d13438",      # Critical - Red
    "Yırtık": "#d13438",             # Critical - Red
    "Leke": "#f7630c",               # Warning - Orange
    "Renk Uyuşmazlığı": "#ffc83d",   # Caution - Yellow
    "Renk Uyumsuzluğu": "#ffc83d",   # Caution - Yellow
    "Dokuma Hatası": "#f7630c",      # Medium - Orange
    "Temiz": "#0f7b0f",              # Success - Green
}

def get_defect_color(defect_type):
    """Return Windows 11 semantic color for defect type."""
    return DEFECT_COLORS.get(defect_type, "#a0a0a0")
