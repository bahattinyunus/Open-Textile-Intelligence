"""
Detection manager for running fabric scanner in background thread.
Supports both SIMULATION and REAL CAMERA modes.

IMPORTANT: This module now handles TWO distinct modes:
1. SIMULATION: Artificial defect generation (demo/testing)
2. CAMERA: Real camera feed analysis (production use)
"""

import time
import random
from PySide6.QtCore import QThread, Signal
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from defect_scanner import FabricScanner
from constants import ScanMode


class DetectionManager(QThread):
    """
    Runs fabric detection in a background thread.
    Mode-aware: Simulation or Camera.
    """

    # Signals for UI updates
    calibration_progress = Signal(int)  # 0-100
    scanning_progress = Signal(int)     # 0-100
    new_detection = Signal(dict)        # Detection record
    scan_complete = Signal()            # Scan finished
    stats_update = Signal(dict)         # Overall statistics

    def __init__(self, mode=ScanMode.SIMULATION, duration_seconds=10):
        super().__init__()
        self.mode = mode
        self.duration_seconds = duration_seconds
        self.scanner = FabricScanner()
        self.is_running = True

    def run(self):
        """
        Main detection loop.
        Behavior changes based on mode.
        """
        if self.mode == ScanMode.SIMULATION:
            self._run_simulation()
        else:
            # Camera mode is handled by CameraManager
            # This thread just manages simulation mode
            pass

    def _run_simulation(self):
        """
        SIMULATION MODE ONLY:
        Runs artificial defect generation for testing.
        NO real camera input.
        """

        # Phase 1: Calibration (simulated)
        calibration_complete = 0
        while calibration_complete < 100 and self.is_running:
            calibration_complete += 1.5
            self.calibration_progress.emit(min(int(calibration_complete), 100))
            time.sleep(0.02)

        if not self.is_running:
            return

        # Emit completion
        self.calibration_progress.emit(100)
        time.sleep(0.1)

        # Phase 2: Scanning (simulated)
        start_time = time.time()
        frame_count = 0

        while time.time() - start_time < self.duration_seconds and self.is_running:
            # Generate frame ID (SIMULATION)
            frame_id = f"SIM-{10000 + frame_count}"

            # Analyze frame (ARTIFICIAL DEFECTS)
            result = self.scanner.analyze_frame(frame_id)
            self.scanner.scanned_yards += 0.5

            # Create detection record
            detection_record = {
                "timestamp": time.strftime("%H:%M:%S"),
                "frame_id": frame_id,
                "is_defective": result["detected"],
                "status": "KUSUR" if result["detected"] else "TAMAM",
                "defect_type": result.get("type", "-"),
                "confidence": result.get("confidence", 0)
            }

            # Store in scanner history
            self.scanner.detection_history.append(detection_record)

            if result["detected"]:
                self.scanner.defects_found += 1

            # Emit new detection (only defects to reduce noise)
            if result["detected"]:
                self.new_detection.emit(detection_record)

            # Update progress
            elapsed_time = time.time() - start_time
            progress = min(int((elapsed_time / self.duration_seconds) * 100), 100)
            self.scanning_progress.emit(progress)

            # Emit statistics update
            efficiency = max(100 - (self.scanner.defects_found * 2), 0)
            self.stats_update.emit({
                "scanned_yards": self.scanner.scanned_yards,
                "defects_found": self.scanner.defects_found,
                "efficiency": efficiency
            })

            frame_count += 1
            time.sleep(0.1)

        # Scan complete
        self.scanning_progress.emit(100)
        self.scan_complete.emit()

    def stop(self):
        """Stop the detection process."""
        self.is_running = False
        self.wait()  # Wait for thread to finish
