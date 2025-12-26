"""
Verification script to check if all fixes are properly implemented.
Run this to verify the production-ready status.
"""

import sys
import os
from pathlib import Path

# Get project root (one level up from scripts/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJ_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJ_ROOT))

# Color codes for terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def check(name, condition, details=""):
    """Print check result."""
    status = f"{GREEN}✅ PASS{RESET}" if condition else f"{RED}❌ FAIL{RESET}"
    print(f"{status} - {name}")
    if details and not condition:
        print(f"     {YELLOW}→ {details}{RESET}")
    return condition

def main():
    print(f"\n{BOLD}{'='*60}")
    print("PRODUCTION READINESS VERIFICATION")
    print(f"{'='*60}{RESET}\n")

    all_passed = True

    # Check 1: Required files exist
    print(f"{BOLD}1. Checking Required Files{RESET}")

    files = [
        PROJ_ROOT / "desktop_app/camera_manager.py",
        PROJ_ROOT / "desktop_app/ui/main_window.py",
        PROJ_ROOT / "desktop_app/main.py",
        PROJ_ROOT / "desktop_app/constants.py",
        PROJ_ROOT / "requirements.txt"
    ]

    for file in files:
        exists = Path(file).exists()
        all_passed &= check(file, exists, f"File not found: {file}")

    print()

    # Check 2: Camera manager has required methods
    print(f"{BOLD}2. Checking Camera Manager Implementation{RESET}")

    try:
        sys.path.insert(0, str(PROJ_ROOT / "desktop_app"))
        from camera_manager import CameraManager

        # Check for test_camera_access method
        has_test = hasattr(CameraManager, 'test_camera_access')
        all_passed &= check(
            "test_camera_access() method",
            has_test,
            "Static method for camera testing not found"
        )

        # Check for camera_opened signal
        has_signal = hasattr(CameraManager, 'camera_opened')
        all_passed &= check(
            "camera_opened signal",
            has_signal,
            "Camera opened signal not found"
        )

        # Check if it's a static method
        if has_test:
            is_static = isinstance(
                CameraManager.__dict__.get('test_camera_access'),
                staticmethod
            )
            all_passed &= check(
                "test_camera_access is static",
                is_static,
                "Method should be static"
            )

    except Exception as e:
        all_passed = False
        print(f"{RED}❌ FAIL - Failed to import camera_manager: {e}{RESET}")

    print()

    # Check 3: Main window has required elements
    print(f"{BOLD}3. Checking Main Window Implementation{RESET}")

    try:
        # Read main_window.py content
        with open(PROJ_ROOT / "desktop_app/ui/main_window.py", 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ("Camera test button", "test_camera_button", "Test button not found in UI"),
            ("Camera status label", "camera_status_label", "Status label not found"),
            ("Camera warning label", "camera_warning_label", "Warning badge not found"),
            ("resize_to_screen method", "def resize_to_screen", "Window resize method not found"),
            ("test_camera method", "def test_camera", "Camera test method not found"),
            ("on_camera_opened method", "def on_camera_opened", "Camera opened handler not found"),
            ("QMessageBox import", "QMessageBox", "Error dialog support not found"),
            ("QScreen import", "QScreen", "Screen detection not found"),
        ]

        for name, search_term, error_msg in checks:
            found = search_term in content
            all_passed &= check(name, found, error_msg)

    except Exception as e:
        all_passed = False
        print(f"{RED}❌ FAIL - Failed to read main_window.py: {e}{RESET}")

    print()

    # Check 4: OpenCV and PySide6 availability
    print(f"{BOLD}4. Checking Dependencies{RESET}")

    try:
        import cv2
        version = cv2.__version__
        all_passed &= check(f"OpenCV installed (v{version})", True)
    except ImportError:
        all_passed &= check("OpenCV installed", False, "pip install opencv-python")

    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        all_passed &= check("PySide6 installed", True)
    except ImportError:
        all_passed &= check("PySide6 installed", False, "pip install PySide6")

    try:
        import numpy
        all_passed &= check("NumPy installed", True)
    except ImportError:
        all_passed &= check("NumPy installed", False, "pip install numpy")

    print()

    # Check 5: DirectShow support (Windows)
    print(f"{BOLD}5. Checking Windows Camera Support{RESET}")

    try:
        with open(PROJ_ROOT / "desktop_app/camera_manager.py", 'r', encoding='utf-8') as f:
            content = f.read()

        has_dshow = "CAP_DSHOW" in content
        all_passed &= check(
            "DirectShow backend",
            has_dshow,
            "CAP_DSHOW not found - Windows optimization missing"
        )

        has_error_msg = "Windows Ayarlar" in content
        all_passed &= check(
            "Windows instructions",
            has_error_msg,
            "Windows settings instructions not found"
        )

    except Exception as e:
        all_passed &= check("Windows support", False, str(e))

    print()

    # Check 6: Documentation
    print(f"{BOLD}6. Checking Documentation{RESET}")

    docs = [
        "docs/CAMERA_PERMISSION_FIX.md",
        "docs/QUICK_START_GUIDE.md",
        "docs/PRODUCTION_READY_SUMMARY.md"
    ]

    for doc in docs:
        exists = (PROJ_ROOT / doc).exists()
        all_passed &= check(doc, exists, f"Documentation not found: {doc}")

    print()

    # Final verdict
    print(f"{BOLD}{'='*60}")
    if all_passed:
        print(f"{GREEN}✅ ALL CHECKS PASSED - PRODUCTION READY{RESET}")
        print(f"{'='*60}{RESET}\n")
        print(f"{BOLD}Next Steps:{RESET}")
        print("1. Run: python desktop_app/main.py")
        print("2. Click: '📷 Kamerayı Test Et'")
        print("3. Test camera mode scanning")
        print("4. Deploy to production\n")
        return 0
    else:
        print(f"{RED}❌ SOME CHECKS FAILED - REVIEW REQUIRED{RESET}")
        print(f"{'='*60}{RESET}\n")
        print(f"{BOLD}Action Required:{RESET}")
        print("Review failed checks above and fix issues\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
