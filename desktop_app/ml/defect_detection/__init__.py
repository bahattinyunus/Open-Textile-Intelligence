"""
Defect Detection Module for Textile Inspection.

PHASE 1 (CURRENT):
- Uses pretrained deep learning model (EfficientNet-B0)
- Adapted for textile defect classification
- Real neural network inference (NOT random logic)

PHASE 2 (FUTURE):
- Replace with textile-specific YOLO/Faster R-CNN
- Add segmentation capabilities
- Train on custom textile defect dataset

Detects:
- Leke (stain)
- Delik (hole) - STRUCTURAL DEFECT
- Yırtık (tear) - STRUCTURAL DEFECT
- İplik Kopması (thread break)
- Renk Uyumsuzluğu (color mismatch)
- Dokuma Hatası (weaving defect)
"""

from .model import DefectDetectionModel
from .inference import DefectDetector

__all__ = ['DefectDetectionModel', 'DefectDetector']
