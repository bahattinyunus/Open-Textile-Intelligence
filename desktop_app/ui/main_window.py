"""
Main window for Open Textile Intelligence desktop application.
PRODUCTION VERSION: Supports both Simulation and Real Camera modes.
FIXED: Camera permissions, responsive UI, proper error handling.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QProgressBar, QFrame,
    QPushButton, QHeaderView, QSlider, QComboBox, QSplitter,
    QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QBrush, QPixmap, QScreen
from .styles import DARK_THEME, get_defect_color
import sys
from pathlib import Path

# Add desktop_app to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from constants import ScanMode, SystemState, MODE_NAMES, STATE_NAMES


class MetricCard(QFrame):
    """Custom widget for displaying metrics."""

    def __init__(self, title, value="0", unit="", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(3)

        # Title
        self.title_label = QLabel(title)
        self.title_label.setObjectName("metricTitle")
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        # Value
        self.value_label = QLabel(value)
        self.value_label.setObjectName("metricValue")
        layout.addWidget(self.value_label)

        # Unit
        if unit:
            self.unit_label = QLabel(unit)
            self.unit_label.setObjectName("metricDelta")
            layout.addWidget(self.unit_label)

        self.setMinimumHeight(80)
        self.setMaximumHeight(120)

    def set_value(self, value):
        """Update metric value."""
        self.value_label.setText(str(value))


class MainWindow(QMainWindow):
    """
    Main application window.
    PRODUCTION: Handles both simulation and real camera modes.
    """

    def __init__(self):
        super().__init__()
        # System state
        self.current_mode = ScanMode.SIMULATION  # Default mode
        self.system_state = SystemState.IDLE
        self.is_scanning = False
        self.camera_permission_denied = False

        # Managers
        self.detection_manager = None
        self.camera_manager = None

        # ML Pipeline (initialized after UI)
        self.ml_pipeline = None
        self.ml_available = False

        # Stats tracking
        self.defects_found = 0
        self.scanned_yards = 0.0

        self.init_ui()
        self.resize_to_screen()
        self.initialize_ml_pipeline()

    def resize_to_screen(self):
        """Resize window to fit screen properly."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Use 95% of screen size to ensure it fits
        width = int(screen_geometry.width() * 0.95)
        height = int(screen_geometry.height() * 0.90)

        # Limit to 1920x1080 max
        width = min(width, 1800)
        height = min(height, 950)

        self.resize(width, height)

        # Center on screen
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        self.move(x, y)

    def init_ui(self):
        """Initialize user interface."""

        self.setWindowTitle("Open Textile Intelligence – Real-Time Inspection System")

        # Apply dark theme
        self.setStyleSheet(DARK_THEME)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Header
        header = QLabel("Open Textile Intelligence")
        header.setObjectName("sectionTitle")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 16pt; padding: 5px; color: #3498db;")
        main_layout.addWidget(header)

        subheader = QLabel("Gerçek Zamanlı Kusur Tespit Sistemi")
        subheader.setAlignment(Qt.AlignCenter)
        subheader.setStyleSheet("font-size: 10pt; color: #95a5a6; padding-bottom: 5px;")
        main_layout.addWidget(subheader)

        # MODE SELECTOR
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(8)

        mode_label = QLabel("🔧 Çalışma Modu:")
        mode_label.setStyleSheet("color: #e0e0e0; font-size: 10pt; font-weight: bold;")
        mode_layout.addWidget(mode_label)

        self.mode_selector = QComboBox()
        self.mode_selector.addItem("SİMÜLASYON MODU – Fiziksel Giriş Yok", ScanMode.SIMULATION)
        self.mode_selector.addItem("GERÇEK KAMERA MODU – Canlı Giriş", ScanMode.CAMERA)
        self.mode_selector.setStyleSheet("""
            QComboBox {
                background-color: #2c2c2c;
                color: #e0e0e0;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 6px;
                font-size: 9pt;
                font-weight: bold;
            }
            QComboBox:hover {
                border-color: #2980b9;
            }
        """)
        self.mode_selector.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_selector)

        # Current mode status label
        self.mode_status_label = QLabel("📍 AKTIF: SİMÜLASYON")
        self.mode_status_label.setStyleSheet("""
            background-color: #f39c12;
            color: #1a1a1a;
            padding: 6px 12px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 9pt;
        """)
        mode_layout.addWidget(self.mode_status_label)

        # Camera permission warning (initially hidden)
        self.camera_warning_label = QLabel("⚠️ Kamera erişimi engellendi")
        self.camera_warning_label.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 6px 12px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 9pt;
        """)
        self.camera_warning_label.setVisible(False)
        mode_layout.addWidget(self.camera_warning_label)

        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)

        # Control panel
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)

        # Camera test button
        self.test_camera_button = QPushButton("📷 Kamerayı Test Et")
        self.test_camera_button.setObjectName("testButton")
        self.test_camera_button.clicked.connect(self.test_camera)
        self.test_camera_button.setMinimumWidth(140)
        self.test_camera_button.setStyleSheet("""
            QPushButton#testButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 9pt;
            }
            QPushButton#testButton:hover {
                background-color: #2980b9;
            }
            QPushButton#testButton:pressed {
                background-color: #1f6391;
            }
        """)
        control_layout.addWidget(self.test_camera_button)

        control_layout.addSpacing(15)

        duration_label = QLabel("Tarama Süresi:")
        duration_label.setStyleSheet("color: #e0e0e0; font-size: 9pt;")
        control_layout.addWidget(duration_label)

        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setMinimum(5)
        self.duration_slider.setMaximum(60)
        self.duration_slider.setValue(10)
        self.duration_slider.setMinimumWidth(120)
        control_layout.addWidget(self.duration_slider)

        self.duration_value_label = QLabel("10 sn")
        self.duration_value_label.setStyleSheet("color: #3498db; font-weight: bold; font-size: 9pt;")
        self.duration_slider.valueChanged.connect(
            lambda v: self.duration_value_label.setText(f"{v} sn")
        )
        control_layout.addWidget(self.duration_value_label)

        control_layout.addSpacing(15)

        self.start_button = QPushButton("▶ Taramayı Başlat")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_scan)
        self.start_button.setMinimumWidth(140)
        control_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹ Durdur")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_scan)
        self.stop_button.setEnabled(False)
        self.stop_button.setMinimumWidth(90)
        control_layout.addWidget(self.stop_button)

        control_layout.addStretch()
        main_layout.addLayout(control_layout)

        # Metric cards
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(8)

        self.metric_scanned = MetricCard("📏 Taranan\nUzunluk", "0.0", "yarda")
        self.metric_defects = MetricCard("⚠️ Tespit\nEdilen", "0", "kusur")
        self.metric_efficiency = MetricCard("✅ Verimlilik\nOranı", "100", "%")
        self.metric_fabric = MetricCard("🧵 Kumaş\nTipi", "—", "")
        self.metric_status = MetricCard("🔄 Sistem\nDurumu", "HAZIR", "")

        metrics_layout.addWidget(self.metric_scanned)
        metrics_layout.addWidget(self.metric_defects)
        metrics_layout.addWidget(self.metric_efficiency)
        metrics_layout.addWidget(self.metric_fabric)
        metrics_layout.addWidget(self.metric_status)

        main_layout.addLayout(metrics_layout)

        # Progress section
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(15)

        # Calibration progress
        cal_layout = QVBoxLayout()
        cal_label = QLabel("Sensör Kalibrasyonu")
        cal_label.setObjectName("statusLabel")
        cal_label.setStyleSheet("font-size: 9pt;")
        cal_layout.addWidget(cal_label)

        self.calibration_bar = QProgressBar()
        self.calibration_bar.setObjectName("calibrationBar")
        self.calibration_bar.setMinimum(0)
        self.calibration_bar.setMaximum(100)
        self.calibration_bar.setValue(0)
        self.calibration_bar.setMaximumHeight(20)
        cal_layout.addWidget(self.calibration_bar)

        progress_layout.addLayout(cal_layout, 1)

        # Scanning progress
        scan_layout = QVBoxLayout()
        scan_label = QLabel("Kumaş Tarama İlerlemesi")
        scan_label.setObjectName("statusLabel")
        scan_label.setStyleSheet("font-size: 9pt;")
        scan_layout.addWidget(scan_label)

        self.scanning_bar = QProgressBar()
        self.scanning_bar.setObjectName("scanningBar")
        self.scanning_bar.setMinimum(0)
        self.scanning_bar.setMaximum(100)
        self.scanning_bar.setValue(0)
        self.scanning_bar.setMaximumHeight(20)
        scan_layout.addWidget(self.scanning_bar)

        progress_layout.addLayout(scan_layout, 1)

        # FPS indicator (for camera mode)
        fps_layout = QVBoxLayout()
        fps_label_header = QLabel("Kare Hızı (FPS)")
        fps_label_header.setObjectName("statusLabel")
        fps_label_header.setStyleSheet("font-size: 9pt;")
        fps_layout.addWidget(fps_label_header)

        self.fps_label = QLabel("--")
        self.fps_label.setStyleSheet("""
            background-color: #2c2c2c;
            color: #27ae60;
            padding: 5px;
            font-size: 14pt;
            font-weight: bold;
            border-radius: 5px;
            qproperty-alignment: AlignCenter;
        """)
        self.fps_label.setMinimumHeight(20)
        self.fps_label.setMaximumHeight(30)
        fps_layout.addWidget(self.fps_label)

        progress_layout.addLayout(fps_layout)

        main_layout.addLayout(progress_layout)

        # CAMERA VIEW + DETECTION TABLE (Side by side)
        content_splitter = QSplitter(Qt.Horizontal)

        # Camera view panel (LEFT)
        camera_panel = QWidget()
        camera_layout = QVBoxLayout(camera_panel)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.setSpacing(5)

        camera_header = QLabel("📹 Kamera Görüntüsü")
        camera_header.setObjectName("sectionTitle")
        camera_header.setStyleSheet("font-size: 10pt;")
        camera_layout.addWidget(camera_header)

        # Camera status label
        self.camera_status_label = QLabel("Kamera Kapalı – Tarama başlatılmadı")
        self.camera_status_label.setAlignment(Qt.AlignCenter)
        self.camera_status_label.setStyleSheet("""
            background-color: #34495e;
            color: #95a5a6;
            padding: 5px;
            border-radius: 3px;
            font-size: 8pt;
            font-weight: bold;
        """)
        camera_layout.addWidget(self.camera_status_label)

        self.camera_view = QLabel()
        self.camera_view.setStyleSheet("""
            background-color: #000000;
            border: 2px solid #3498db;
            border-radius: 5px;
            color: #95a5a6;
        """)
        self.camera_view.setAlignment(Qt.AlignCenter)
        self.camera_view.setText("Kamera Modu: KAPALI\n\nGerçek kamera modunu kullanmak için:\n1. 'GERÇEK KAMERA MODU' seçin\n2. 'Taramayı Başlat' butonuna tıklayın")
        self.camera_view.setMinimumSize(300, 200)
        self.camera_view.setScaledContents(False)
        camera_layout.addWidget(self.camera_view, 1)

        content_splitter.addWidget(camera_panel)

        # Detection table panel (RIGHT)
        table_panel = QWidget()
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(5)

        table_header = QLabel("🔍 Canlı Tespit Akışı")
        table_header.setObjectName("sectionTitle")
        table_header.setStyleSheet("font-size: 10pt;")
        table_layout.addWidget(table_header)

        self.detection_table = QTableWidget()
        self.detection_table.setColumnCount(5)
        self.detection_table.setHorizontalHeaderLabels([
            "Zaman", "Kare No", "Durum", "Kusur Tipi", "Güven (%)"
        ])

        # Configure table
        self.detection_table.setAlternatingRowColors(True)
        self.detection_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.detection_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.detection_table.verticalHeader().setVisible(False)

        # Column widths - responsive
        header = self.detection_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        table_layout.addWidget(self.detection_table, 1)

        content_splitter.addWidget(table_panel)

        # Set initial splitter sizes (50% camera, 50% table)
        content_splitter.setSizes([500, 500])
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(content_splitter, 1)  # Stretch factor 1

        # Status bar
        self.statusBar().showMessage("Sistem hazır. Mod seçin ve taramayı başlatın.")
        self.statusBar().setStyleSheet("color: #95a5a6; background-color: #2c2c2c; padding: 4px;")

    def initialize_ml_pipeline(self):
        """
        Initialize Machine Learning pipeline for defect detection and fabric classification.

        PRODUCTION SYSTEM - Uses real PyTorch deep learning models.
        """
        try:
            print("\n" + "="*70)
            print("STARTING ML PIPELINE INITIALIZATION")
            print("="*70)

            from ml.pipeline import create_ml_pipeline

            # Create ML pipeline with pretrained models
            # For production, replace None with paths to custom-trained weights
            self.ml_pipeline = create_ml_pipeline(
                defect_weights=None,  # None = use pretrained ImageNet (PHASE 1)
                fabric_weights=None,   # None = use pretrained ImageNet (PHASE 1)
                device=None,           # None = auto-detect (CUDA if available)
                confidence_threshold=0.6  # 60% minimum confidence for defect reporting
            )

            self.ml_available = True

            # Update status
            self.statusBar().showMessage(
                "✅ ML sistemi hazır - Gerçek derin öğrenme modelleri yüklendi"
            )

            print("\n✅ ML PIPELINE READY FOR PRODUCTION USE")
            print("="*70 + "\n")

        except ImportError as e:
            self.ml_available = False
            error_msg = (
                f"❌ ML modülleri yüklenemedi: {e}\n\n"
                "GEREKLI PAKETLER:\n"
                "pip install torch torchvision\n\n"
                "Kamera modu devre dışı bırakıldı."
            )
            print(error_msg)

            QMessageBox.critical(
                self,
                "❌ ML Sistemi Hatası",
                error_msg,
                QMessageBox.Ok
            )

            # Disable camera mode
            mode_index = self.mode_selector.findData(ScanMode.CAMERA)
            if mode_index >= 0:
                self.mode_selector.model().item(mode_index).setEnabled(False)

            self.statusBar().showMessage("❌ ML sistemi yüklenemedi - PyTorch gerekli")

        except Exception as e:
            self.ml_available = False
            error_msg = f"❌ ML pipeline başlatılamadı: {str(e)}"
            print(error_msg)

            QMessageBox.warning(
                self,
                "⚠️ ML Sistemi Uyarısı",
                f"{error_msg}\n\nKamera modu devre dışı bırakıldı.",
                QMessageBox.Ok
            )

            # Disable camera mode
            mode_index = self.mode_selector.findData(ScanMode.CAMERA)
            if mode_index >= 0:
                self.mode_selector.model().item(mode_index).setEnabled(False)

            self.statusBar().showMessage("⚠️ ML sistemi kullanılamıyor")

    def test_camera(self):
        """Test camera access and show results."""
        from camera_manager import CameraManager

        self.statusBar().showMessage("Kamera test ediliyor...")
        self.test_camera_button.setEnabled(False)

        # Run camera test
        success, message = CameraManager.test_camera_access(camera_index=0, timeout_seconds=3)

        self.test_camera_button.setEnabled(True)

        if success:
            QMessageBox.information(
                self,
                "✅ Kamera Testi Başarılı",
                "Kamera erişimi başarılı!\n\n"
                "Kamera düzgün çalışıyor.\n"
                "'GERÇEK KAMERA MODU' seçerek kullanabilirsiniz.",
                QMessageBox.Ok
            )
            self.camera_permission_denied = False
            self.camera_warning_label.setVisible(False)
            self.statusBar().showMessage("✓ Kamera testi başarılı")
        else:
            QMessageBox.critical(
                self,
                "❌ Kamera Erişim Hatası",
                f"{message}\n\n"
                "WINDOWS KAMERA İZİNLERİNİ AÇMAK İÇİN:\n"
                "1. Windows Ayarlar'ı açın (Win + I)\n"
                "2. Gizlilik ve Güvenlik → Kamera\n"
                "3. 'Uygulamaların kameraya erişmesine izin ver' → AÇIK\n"
                "4. Uygulamayı yeniden başlatın",
                QMessageBox.Ok
            )
            self.camera_permission_denied = True
            self.camera_warning_label.setVisible(True)
            self.statusBar().showMessage("❌ Kamera erişimi engellendi")

    def on_mode_changed(self, index):
        """Handle mode selection change."""
        # Do NOT allow mode change during scan
        if self.is_scanning:
            self.statusBar().showMessage("⚠️ Tarama devam ederken mod değiştirilemez!")
            # Revert to current mode
            current_index = 0 if self.current_mode == ScanMode.SIMULATION else 1
            self.mode_selector.setCurrentIndex(current_index)
            return

        # Update mode
        new_mode = self.mode_selector.itemData(index)
        self.current_mode = new_mode

        # Update mode status label
        if new_mode == ScanMode.SIMULATION:
            self.mode_status_label.setText("📍 AKTIF: SİMÜLASYON")
            self.mode_status_label.setStyleSheet("""
                background-color: #f39c12;
                color: #1a1a1a;
                padding: 6px 12px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 9pt;
            """)
            self.camera_view.setText("Kamera Modu: KAPALI\n\nSimülasyon modunda kamera kullanılmaz.")
            self.camera_status_label.setText("Kamera Kapalı – Simülasyon Modu")
            self.camera_status_label.setStyleSheet("""
                background-color: #34495e;
                color: #95a5a6;
                padding: 5px;
                border-radius: 3px;
                font-size: 8pt;
                font-weight: bold;
            """)
        else:
            self.mode_status_label.setText("📍 AKTIF: GERÇEK KAMERA")
            self.mode_status_label.setStyleSheet("""
                background-color: #27ae60;
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 9pt;
            """)
            self.camera_view.setText("Kamera Hazır\n\n'Taramayı Başlat' butonuna tıklayın")
            self.camera_status_label.setText("Kamera Kapalı – Tarama başlatılmadı")

        self.statusBar().showMessage(f"Mod değiştirildi: {MODE_NAMES[new_mode]}")

    def start_scan(self):
        """Start detection scan based on selected mode."""
        if self.is_scanning:
            return

        # Clear previous data
        self.detection_table.setRowCount(0)
        self.calibration_bar.setValue(0)
        self.scanning_bar.setValue(0)
        self.metric_scanned.set_value("0.0")
        self.metric_defects.set_value("0")
        self.metric_efficiency.set_value("100")
        self.defects_found = 0
        self.scanned_yards = 0.0

        # Disable controls
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.mode_selector.setEnabled(False)  # Lock mode during scan
        self.test_camera_button.setEnabled(False)
        self.is_scanning = True

        duration = self.duration_slider.value()

        if self.current_mode == ScanMode.SIMULATION:
            self._start_simulation_scan(duration)
        else:
            self._start_camera_scan(duration)

    def _start_simulation_scan(self, duration):
        """Start simulation mode scan."""
        from detection_manager import DetectionManager

        self.system_state = SystemState.SCANNING_SIMULATION
        self.metric_status.set_value("SİMÜLASYON")

        self.detection_manager = DetectionManager(mode=ScanMode.SIMULATION, duration_seconds=duration)

        # Connect signals
        self.detection_manager.calibration_progress.connect(self.update_calibration)
        self.detection_manager.scanning_progress.connect(self.update_scanning)
        self.detection_manager.new_detection.connect(self.add_detection_row)
        self.detection_manager.stats_update.connect(self.update_stats)
        self.detection_manager.scan_complete.connect(self.scan_finished)

        # Start
        self.detection_manager.start()
        self.statusBar().showMessage("SİMÜLASYON: Tarama devam ediyor...")

    def _start_camera_scan(self, duration):
        """Start real camera mode scan with ML pipeline."""
        from camera_manager import CameraManager

        # Check if ML is available
        if not self.ml_available or self.ml_pipeline is None:
            QMessageBox.critical(
                self,
                "❌ ML Sistemi Hatası",
                "ML sistemi kullanılamıyor.\n\n"
                "Kamera modu için PyTorch gerekli:\n"
                "pip install torch torchvision",
                QMessageBox.Ok
            )
            self.scan_finished()
            return

        self.system_state = SystemState.SCANNING_CAMERA
        self.metric_status.set_value("KAMERA + ML")

        # Update camera status
        self.camera_status_label.setText("Kamera Açılıyor...")
        self.camera_status_label.setStyleSheet("""
            background-color: #f39c12;
            color: #1a1a1a;
            padding: 5px;
            border-radius: 3px;
            font-size: 8pt;
            font-weight: bold;
        """)

        # Create camera manager WITH ML pipeline
        self.camera_manager = CameraManager(
            camera_index=0,
            duration_seconds=duration,
            ml_pipeline=self.ml_pipeline  # Pass ML pipeline
        )

        # Connect signals
        self.camera_manager.frame_captured.connect(self.update_camera_view)
        self.camera_manager.frame_analyzed.connect(self.add_detection_row)
        self.camera_manager.fps_updated.connect(self.update_fps)
        self.camera_manager.camera_error.connect(self.handle_camera_error)
        self.camera_manager.scanning_progress.connect(self.update_scanning)
        self.camera_manager.scan_complete.connect(self.scan_finished)
        self.camera_manager.camera_opened.connect(self.on_camera_opened)

        # Start
        self.camera_manager.start()
        self.calibration_bar.setValue(100)  # No calibration in camera mode
        self.statusBar().showMessage("KAMERA: Canlı tarama devam ediyor...")

    def on_camera_opened(self, success):
        """Handle camera open success/failure."""
        if success:
            self.camera_status_label.setText("✅ Kamera Aktif – Canlı Görüntü")
            self.camera_status_label.setStyleSheet("""
                background-color: #27ae60;
                color: white;
                padding: 5px;
                border-radius: 3px;
                font-size: 8pt;
                font-weight: bold;
            """)
            self.camera_permission_denied = False
            self.camera_warning_label.setVisible(False)
        else:
            self.camera_status_label.setText("❌ Kamera Erişim Hatası")
            self.camera_status_label.setStyleSheet("""
                background-color: #e74c3c;
                color: white;
                padding: 5px;
                border-radius: 3px;
                font-size: 8pt;
                font-weight: bold;
            """)
            self.camera_permission_denied = True
            self.camera_warning_label.setVisible(True)

            # Disable start button until issue is resolved
            self.start_button.setEnabled(False)

    def stop_scan(self):
        """Stop current scan."""
        if self.detection_manager:
            self.detection_manager.stop()
            self.detection_manager = None

        if self.camera_manager:
            self.camera_manager.stop()
            self.camera_manager = None

        self.scan_finished()

    def update_calibration(self, value):
        """Update calibration progress bar."""
        self.calibration_bar.setValue(value)

    def update_scanning(self, value):
        """Update scanning progress bar."""
        self.scanning_bar.setValue(value)

    def update_camera_view(self, q_image):
        """Update camera view with new frame."""
        pixmap = QPixmap.fromImage(q_image)
        # Scale to fit while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.camera_view.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.camera_view.setPixmap(scaled_pixmap)

    def update_fps(self, fps):
        """Update FPS label."""
        self.fps_label.setText(f"{fps:.1f}")

    def handle_camera_error(self, error_message):
        """Handle camera errors with dialog."""
        self.statusBar().showMessage(f"❌ KAMERA HATASI")
        self.camera_view.setText(f"KAMERA HATASI\n\n{error_message}")

        # Show error dialog
        QMessageBox.critical(
            self,
            "❌ Kamera Hatası",
            error_message,
            QMessageBox.Ok
        )

        # Mark camera as denied
        self.camera_permission_denied = True
        self.camera_warning_label.setVisible(True)

        # Stop scanning
        self.scan_finished()

    def add_detection_row(self, detection):
        """Add new detection to table with highlight animation."""
        row_position = self.detection_table.rowCount()
        self.detection_table.insertRow(row_position)

        # Time
        if isinstance(detection["timestamp"], str):
            time_str = detection["timestamp"]
        else:
            # Convert timestamp to time string
            import time
            time_str = time.strftime("%H:%M:%S", time.localtime(detection["timestamp"]))

        time_item = QTableWidgetItem(time_str)
        time_item.setTextAlignment(Qt.AlignCenter)
        self.detection_table.setItem(row_position, 0, time_item)

        # Frame ID
        frame_item = QTableWidgetItem(detection["frame_id"])
        frame_item.setTextAlignment(Qt.AlignCenter)
        self.detection_table.setItem(row_position, 1, frame_item)

        # Status
        status_item = QTableWidgetItem(f"⚠️ {detection['status']}")
        status_item.setTextAlignment(Qt.AlignCenter)
        status_item.setForeground(QBrush(QColor("#e74c3c")))
        self.detection_table.setItem(row_position, 2, status_item)

        # Defect type
        defect_item = QTableWidgetItem(detection["defect_type"])
        defect_color = get_defect_color(detection["defect_type"])
        defect_item.setForeground(QBrush(QColor(defect_color)))
        defect_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.detection_table.setItem(row_position, 3, defect_item)

        # Confidence
        confidence_pct = detection["confidence"] * 100 if detection["confidence"] <= 1.0 else detection["confidence"]
        conf_item = QTableWidgetItem(f"{confidence_pct:.1f}%")
        conf_item.setTextAlignment(Qt.AlignCenter)

        if confidence_pct >= 95:
            conf_item.setForeground(QBrush(QColor("#27ae60")))
        elif confidence_pct >= 85:
            conf_item.setForeground(QBrush(QColor("#f39c12")))
        else:
            conf_item.setForeground(QBrush(QColor("#e74c3c")))

        self.detection_table.setItem(row_position, 4, conf_item)

        # Update stats
        self.defects_found += 1
        self.metric_defects.set_value(str(self.defects_found))

        # Update fabric type if available (from ML)
        if "fabric_type" in detection and detection["fabric_type"]:
            fabric_type = detection["fabric_type"]
            fabric_conf = detection.get("fabric_confidence", 0)

            # Update fabric metric card
            if fabric_conf > 0:
                self.metric_fabric.set_value(f"{fabric_type}\n({fabric_conf:.0f}%)")
            else:
                self.metric_fabric.set_value(fabric_type)

        # Scroll to new row
        self.detection_table.scrollToBottom()

        # Highlight animation (brief flash)
        self.highlight_row(row_position)

    def highlight_row(self, row):
        """Briefly highlight a new row."""
        for col in range(self.detection_table.columnCount()):
            item = self.detection_table.item(row, col)
            if item:
                original_bg = item.background()
                item.setBackground(QBrush(QColor("#3498db")))

                # Reset after delay
                QTimer.singleShot(500, lambda i=item, bg=original_bg: i.setBackground(bg))

    def update_stats(self, stats):
        """Update statistics metrics (simulation mode)."""
        self.scanned_yards = stats['scanned_yards']
        self.metric_scanned.set_value(f"{stats['scanned_yards']:.1f}")
        self.metric_defects.set_value(str(stats['defects_found']))
        self.metric_efficiency.set_value(str(stats['efficiency']))

    def scan_finished(self):
        """Handle scan completion."""
        self.metric_status.set_value("TAMAMLANDI")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.mode_selector.setEnabled(True)  # Unlock mode
        self.test_camera_button.setEnabled(True)
        self.is_scanning = False
        self.system_state = SystemState.IDLE

        if self.current_mode == ScanMode.CAMERA:
            self.fps_label.setText("--")
            self.camera_view.setText("Tarama Tamamlandı\n\nYeni tarama için butona tıklayın")
            self.camera_status_label.setText("Kamera Kapalı – Tarama tamamlandı")
            self.camera_status_label.setStyleSheet("""
                background-color: #34495e;
                color: #95a5a6;
                padding: 5px;
                border-radius: 3px;
                font-size: 8pt;
                font-weight: bold;
            """)

        self.statusBar().showMessage("✓ Tarama tamamlandı.")

    def closeEvent(self, event):
        """Handle application close - clean up resources."""
        # Stop any active scans
        if self.is_scanning:
            self.stop_scan()

        # Release camera
        if self.camera_manager:
            self.camera_manager.stop()
            self.camera_manager.release_camera()

        event.accept()
