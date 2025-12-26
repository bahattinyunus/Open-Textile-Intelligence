"""
Machine Learning Module for Open Textile Intelligence.

This module provides real deep learning-based textile inspection capabilities:
- Defect detection (yırtık, delik, leke, etc.)
- Fabric type classification (pamuk, denim, örme, etc.)

PRODUCTION SYSTEM - NOT A DEMO
Uses PyTorch with pretrained models adapted for textile inspection.
"""

from .pipeline import TextileInspectionPipeline

__all__ = ['TextileInspectionPipeline']
