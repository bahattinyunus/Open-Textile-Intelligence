"""
Dark industrial theme for Open Textile Intelligence desktop application.
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1a1a;
}

QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

/* Metric Cards */
QFrame#metricCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #2d3e50, stop:1 #34495e);
    border-radius: 8px;
    border: 1px solid #34495e;
    padding: 15px;
    margin: 5px;
}

QLabel#metricTitle {
    color: #95a5a6;
    font-size: 9pt;
    font-weight: bold;
}

QLabel#metricValue {
    color: #ecf0f1;
    font-size: 24pt;
    font-weight: bold;
}

QLabel#metricDelta {
    color: #27ae60;
    font-size: 9pt;
}

/* Table */
QTableWidget {
    background-color: #2c2c2c;
    alternate-background-color: #323232;
    color: #e0e0e0;
    gridline-color: #404040;
    border: 1px solid #404040;
    border-radius: 4px;
    selection-background-color: #3498db;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #3498db;
    color: white;
}

QHeaderView::section {
    background-color: #34495e;
    color: #ecf0f1;
    padding: 10px;
    border: none;
    font-weight: bold;
    font-size: 10pt;
}

/* Progress Bars */
QProgressBar {
    border: 1px solid #404040;
    border-radius: 4px;
    text-align: center;
    background-color: #2c2c2c;
    color: #e0e0e0;
    height: 25px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3498db, stop:1 #2980b9);
    border-radius: 3px;
}

QProgressBar#calibrationBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #27ae60, stop:1 #229954);
}

QProgressBar#scanningBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3498db, stop:1 #2874a6);
}

/* Labels */
QLabel#sectionTitle {
    color: #3498db;
    font-size: 12pt;
    font-weight: bold;
    padding: 10px 0px;
}

QLabel#statusLabel {
    color: #95a5a6;
    font-size: 9pt;
    padding: 5px;
}

/* Buttons */
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-size: 10pt;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #7f8c8d;
    color: #bdc3c7;
}

QPushButton#startButton {
    background-color: #27ae60;
}

QPushButton#startButton:hover {
    background-color: #229954;
}

QPushButton#stopButton {
    background-color: #e74c3c;
}

QPushButton#stopButton:hover {
    background-color: #c0392b;
}

/* Scrollbar */
QScrollBar:vertical {
    background-color: #2c2c2c;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# Color codes for defect severity
DEFECT_COLORS = {
    "Delik": "#e74c3c",              # Critical - Red
    "İplik Kopması": "#e74c3c",      # Critical - Red
    "Leke": "#f39c12",               # Warning - Orange
    "Renk Uyuşmazlığı": "#f1c40f",   # Warning - Yellow
    "Dokuma Hatası": "#e67e22",      # Medium - Orange
}

def get_defect_color(defect_type):
    """Return color code for defect type."""
    return DEFECT_COLORS.get(defect_type, "#95a5a6")
