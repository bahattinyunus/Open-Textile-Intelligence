"""
Constants and enums for Open Textile Intelligence application.
Defines system modes and states for production-level clarity.
"""

from enum import Enum, auto


class ScanMode(Enum):
    """
    Scanning mode selector.
    CRITICAL: This determines whether the system uses real hardware or simulation.
    """
    SIMULATION = auto()  # Artificial defect generation - NO physical input
    CAMERA = auto()      # Real camera feed - ACTUAL hardware input


class SystemState(Enum):
    """
    Current system state.
    Used for proper resource management and UI control.
    """
    IDLE = auto()                 # System ready, no scanning active
    SCANNING_SIMULATION = auto()  # Simulation scan in progress
    SCANNING_CAMERA = auto()      # Camera scan in progress


# Mode display names (Turkish)
MODE_NAMES = {
    ScanMode.SIMULATION: "SİMÜLASYON MODU – Fiziksel Giriş Yok",
    ScanMode.CAMERA: "GERÇEK KAMERA MODU – Canlı Giriş"
}

# State display names (Turkish)
STATE_NAMES = {
    SystemState.IDLE: "HAZIR",
    SystemState.SCANNING_SIMULATION: "SİMÜLASYON DEVAM EDİYOR",
    SystemState.SCANNING_CAMERA: "KAMERA TARANIYOR"
}

# Frame to yards conversion (matches simulation: 0.5 yards/frame)
YARDS_PER_FRAME = 0.5
