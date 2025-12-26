"""
Defect Detection Inference Engine.
Real-time defect detection on camera frames using deep learning.
"""

import torch
import numpy as np
from .model import load_defect_model, DEFECT_CLASSES
from .preprocessing import (
    preprocess_for_defect_detection,
    extract_texture_features,
    enhance_defect_detection
)
from ..shared.transforms import get_transform
from ..shared.utils import get_device


class DefectDetector:
    """
    Real-time defect detection inference engine.

    Uses pretrained deep learning model to detect textile defects.
    PHASE 1: Pretrained ImageNet features (PLACEHOLDER)
    PHASE 2: Custom textile-trained model
    """

    def __init__(self, weights_path=None, device=None, confidence_threshold=0.6):
        """
        Initialize defect detector.

        Args:
            weights_path: Path to model weights (None = use pretrained)
            device: torch.device (None = auto-detect)
            confidence_threshold: Minimum confidence to report defect (0.0-1.0)
        """
        # Get device
        if device is None:
            device = get_device()
        self.device = device

        # Load model
        print(f"🔧 Loading defect detection model on {self.device}...")
        self.model = load_defect_model(weights_path, device)
        self.model.eval()

        # Get transform
        self.transform = get_transform(input_size=224, normalize=True)

        # Confidence threshold
        self.confidence_threshold = confidence_threshold

        print(f"✅ Defect detector ready (threshold: {confidence_threshold:.1%})")

    def detect(self, cv_image, use_texture_enhancement=True):
        """
        Detect defects in camera frame.

        Args:
            cv_image: OpenCV image (BGR numpy array)
            use_texture_enhancement: Whether to use texture features

        Returns:
            dict with:
                - defect_detected: Boolean
                - defect_type: Defect class name or "Temiz"
                - confidence: Confidence percentage (0-100)
                - is_structural: Boolean (for yırtık/delik)
                - severity: "HIGH", "MEDIUM", "LOW"
                - texture_features: dict (if use_texture_enhancement=True)
        """
        # Preprocess image
        with torch.no_grad():
            tensor = preprocess_for_defect_detection(cv_image, self.transform)
            tensor = tensor.to(self.device)

            # Run model inference
            prediction = self.model.predict(tensor)

        # Extract texture features if requested
        texture_features = None
        if use_texture_enhancement:
            texture_features = extract_texture_features(cv_image)

            # Enhance prediction with texture analysis
            prediction = enhance_defect_detection(prediction, texture_features)

        # Determine if defect should be reported
        confidence_decimal = prediction['confidence'] / 100.0
        defect_detected = (
            prediction['is_defective'] and
            confidence_decimal >= self.confidence_threshold
        )

        # Determine severity
        if prediction['is_structural']:
            severity = "HIGH"  # Yırtık, delik are critical
        elif prediction['is_defective']:
            severity = "MEDIUM" if confidence_decimal > 0.8 else "LOW"
        else:
            severity = "NONE"

        result = {
            'defect_detected': defect_detected,
            'defect_type': prediction['class_name'],
            'confidence': prediction['confidence'],
            'is_structural': prediction['is_structural'],
            'severity': severity,
            'class_idx': prediction['class_idx'],
        }

        if texture_features is not None:
            result['texture_features'] = texture_features
            result['texture_confirmed'] = prediction.get('texture_confirmed', False)

        return result

    def detect_batch(self, cv_images):
        """
        Detect defects in batch of images (for future optimization).

        Args:
            cv_images: List of OpenCV images

        Returns:
            list of detection results
        """
        results = []
        for img in cv_images:
            result = self.detect(img)
            results.append(result)

        return results

    def get_defect_classes(self):
        """
        Get list of defect classes.

        Returns:
            list of defect class names
        """
        return DEFECT_CLASSES

    def set_confidence_threshold(self, threshold):
        """
        Update confidence threshold.

        Args:
            threshold: New threshold (0.0-1.0)
        """
        self.confidence_threshold = max(0.0, min(1.0, threshold))
        print(f"Updated confidence threshold: {self.confidence_threshold:.1%}")
