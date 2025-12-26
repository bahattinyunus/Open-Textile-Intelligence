"""
Fabric Type Classification Module.

Classifies fabric types from camera images:
- Pamuk (cotton)
- Denim
- Örme (knit)
- Dokuma (woven)
- Sentetik (synthetic: polyester, nylon, etc.)

PHASE 1 (CURRENT):
- Uses pretrained ResNet-18 with custom head
- Real neural network inference

PHASE 2 (FUTURE):
- Train on custom textile dataset
- Add more fabric subtypes
"""

from .model import FabricClassificationModel
from .inference import FabricClassifier

__all__ = ['FabricClassificationModel', 'FabricClassifier']
