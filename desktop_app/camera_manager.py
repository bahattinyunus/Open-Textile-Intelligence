"""
Real camera manager for Open Textile Intelligence.
Handles OpenCV camera capture in a background thread.

PRODUCTION MODE: Uses REAL ML models for defect detection and fabric classification.
"""

import cv2
import numpy as np
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
from constants import YARDS_PER_FRAME


class CameraManager(QThread):
    """
    Manages real camera capture in background thread.
    Emits frames for UI display and ML-based defect analysis.
    """

    # Signals
    frame_captured = Signal(QImage)  # For UI display
    frame_analyzed = Signal(dict)    # Detection results
    fps_updated = Signal(float)      # Frame rate
    camera_error = Signal(str)       # Error messages
    scanning_progress = Signal(int)  # Progress percentage (0-100)
    scan_complete = Signal()         # Scan finished
    camera_opened = Signal(bool)     # Camera opened successfully
    stats_update = Signal(dict)      # Real-time statistics (matches simulation)

    def __init__(self, camera_index=0, duration_seconds=10, ml_pipeline=None):
        """
        Initialize camera manager.

        Args:
            camera_index: Camera device index
            duration_seconds: Scan duration
            ml_pipeline: TextileInspectionPipeline instance (if None, ML disabled)
        """
        super().__init__()
        self.camera_index = camera_index
        self.duration_seconds = duration_seconds
        self.is_running = False
        self.cap = None
        self.frame_count = 0
        self.clean_frame_count = 0  # Frames without defects

        # ML Pipeline
        self.ml_pipeline = ml_pipeline
        self.ml_enabled = ml_pipeline is not None

        if not self.ml_enabled:
            print("⚠️  Camera manager initialized WITHOUT ML pipeline")
            print("   Defect detection will be disabled")

    @staticmethod
    def test_camera_access(camera_index=0, timeout_seconds=3):
        """
        Test if camera can be accessed.

        Returns:
            tuple: (success: bool, error_message: str)
        """
        try:
            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Windows DirectShow

            if not cap.isOpened():
                return False, f"Kamera açılamadı (İndeks: {camera_index})\n\nOlası sebepler:\n• Kamera bağlı değil\n• Windows kamera izinleri engellendi\n• Başka uygulama kamerayı kullanıyor"

            # Try to read a frame with timeout
            start_time = time.time()
            ret = False
            while time.time() - start_time < timeout_seconds:
                ret, frame = cap.read()
                if ret:
                    break
                time.sleep(0.1)

            cap.release()

            if not ret:
                return False, "Kamera açıldı ama kare okunamadı\n\nOlası sebepler:\n• Kamera arızalı\n• USB bağlantı problemi\n• Sürücü hatası"

            return True, "Kamera erişimi başarılı"

        except Exception as e:
            return False, f"Kamera test hatası:\n{str(e)}"

    def run(self):
        """Main camera capture loop."""
        # Open camera with DirectShow backend (Windows optimized)
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

        # Verify camera opened
        if not self.cap.isOpened():
            error_msg = (
                f"Kamera açılamadı (İndeks: {self.camera_index})\n\n"
                "ÇÖZÜM ADIMLARI:\n"
                "1. Windows Ayarlar → Gizlilik ve Güvenlik → Kamera\n"
                "2. 'Uygulamaların kameraya erişmesine izin ver' → AÇIK\n"
                "3. Başka uygulamaları kapatın (Zoom, Teams, vb.)\n"
                "4. Kamerayı çıkarıp tekrar takın"
            )
            self.camera_error.emit(error_msg)
            self.camera_opened.emit(False)
            return

        # Try to read first frame to verify camera works
        ret, test_frame = self.cap.read()
        if not ret:
            self.cap.release()
            error_msg = (
                "Kamera açıldı ama kare okunamadı\n\n"
                "ÇÖZÜM ADIMLARI:\n"
                "1. USB kablosunu kontrol edin\n"
                "2. Farklı USB port deneyin\n"
                "3. Bilgisayarı yeniden başlatın"
            )
            self.camera_error.emit(error_msg)
            self.camera_opened.emit(False)
            return

        # Camera successfully opened
        self.camera_opened.emit(True)
        self.is_running = True

        start_time = time.time()
        fps_start = time.time()
        fps_frames = 0

        while self.is_running and (time.time() - start_time) < self.duration_seconds:
            ret, frame = self.cap.read()

            if not ret:
                self.camera_error.emit("Kare okunamadı - Kamera bağlantısı koptu")
                break

            self.frame_count += 1

            # Convert frame to QImage for display (BGR → RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Emit frame for UI display
            self.frame_captured.emit(qt_image.copy())

            # Analyze frame for defects using ML
            if self.ml_enabled:
                detection_result = self._analyze_frame_with_ml(frame)

                # Emit detection result if defect found
                if detection_result["is_defective"]:
                    self.frame_analyzed.emit(detection_result)
                else:
                    # Track clean frames for efficiency
                    self.clean_frame_count += 1

            # Calculate FPS
            fps_frames += 1
            if time.time() - fps_start >= 1.0:
                fps = fps_frames / (time.time() - fps_start)
                self.fps_updated.emit(fps)
                fps_frames = 0
                fps_start = time.time()

            # Update scanning progress
            elapsed_time = time.time() - start_time
            progress = min(int((elapsed_time / self.duration_seconds) * 100), 100)
            self.scanning_progress.emit(progress)

            # Emit statistics update (matches simulation pattern)
            scanned_yards = self.frame_count * YARDS_PER_FRAME
            efficiency = int((self.clean_frame_count / self.frame_count) * 100) if self.frame_count > 0 else 100

            self.stats_update.emit({
                'scanned_yards': scanned_yards,
                'defects_found': self.frame_count - self.clean_frame_count,
                'efficiency': efficiency
            })

            # Control frame rate (avoid overwhelming CPU)
            time.sleep(0.033)  # ~30 FPS

        # Cleanup
        # Emit final statistics
        if self.frame_count > 0:
            scanned_yards = self.frame_count * YARDS_PER_FRAME
            efficiency = int((self.clean_frame_count / self.frame_count) * 100)
            self.stats_update.emit({
                'scanned_yards': scanned_yards,
                'defects_found': self.frame_count - self.clean_frame_count,
                'efficiency': efficiency
            })

        self.scanning_progress.emit(100)  # Ensure 100% at end
        self.release_camera()
        self.scan_complete.emit()

    def _analyze_frame_with_ml(self, frame):
        """
        Analyze camera frame using REAL ML models.

        PRODUCTION IMPLEMENTATION:
        - Uses PyTorch deep learning models
        - Performs defect detection
        - Performs fabric classification
        - NO random logic, NO fake outputs

        Args:
            frame: OpenCV frame (BGR numpy array)

        Returns:
            dict: Detection result with ML predictions
        """
        try:
            # Run ML pipeline
            ml_result = self.ml_pipeline.inspect_frame(frame)

            # Create detection record
            detection_record = {
                "timestamp": time.strftime("%H:%M:%S"),
                "frame_id": f"CAM-{self.frame_count:05d}",
                "is_defective": ml_result['defect_detected'],
                "status": "KUSUR" if ml_result['defect_detected'] else "TAMAM",
                "defect_type": ml_result['defect_type'],
                "confidence": ml_result['defect_confidence'],

                # Fabric classification
                "fabric_type": ml_result['fabric_type'],
                "fabric_confidence": ml_result['fabric_confidence'],

                # Severity and structural info
                "is_structural": ml_result['is_structural'],
                "severity": ml_result['severity'],

                # Performance
                "inference_time_ms": ml_result['inference_time_ms'],

                # Additional details
                "texture_features": ml_result.get('texture_features', {}),
                "fabric_features": ml_result.get('fabric_features', {}),
            }

            return detection_record

        except Exception as e:
            # If ML fails, return error record
            print(f"❌ ML inference error: {e}")
            return {
                "timestamp": time.strftime("%H:%M:%S"),
                "frame_id": f"CAM-{self.frame_count:05d}",
                "is_defective": False,
                "status": "ML HATASI",
                "defect_type": f"ML Error: {str(e)}",
                "confidence": 0.0,
                "fabric_type": "Bilinmiyor",
                "fabric_confidence": 0.0,
                "is_structural": False,
                "severity": "NONE",
            }

    def stop(self):
        """Stop camera capture."""
        self.is_running = False
        self.wait()  # Wait for thread to finish

    def release_camera(self):
        """Release camera resources properly."""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
