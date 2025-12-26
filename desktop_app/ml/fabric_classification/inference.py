"""
Fabric Classification Inference Engine.
Real-time fabric type classification on camera frames using deep learning.
"""

import torch
from .model import load_fabric_model, FABRIC_CLASSES
from .preprocessing import (
    preprocess_for_fabric_classification,
    extract_fabric_features,
    enhance_fabric_classification
)
from ..shared.transforms import get_transform
from ..shared.utils import get_device


class FabricClassifier:
    """
    Real-time fabric classification inference engine.

    Uses pretrained deep learning model to classify fabric types.
    PHASE 1: Pretrained ImageNet features (PLACEHOLDER)
    PHASE 2: Custom textile-trained model
    """

    def __init__(self, weights_path=None, device=None):
        """
        Initialize fabric classifier.

        Args:
            weights_path: Path to model weights (None = use pretrained)
            device: torch.device (None = auto-detect)
        """
        # Get device
        if device is None:
            device = get_device()
        self.device = device

        # Load model
        print(f"🔧 Loading fabric classification model on {self.device}...")
        self.model = load_fabric_model(weights_path, device)
        self.model.eval()

        # Get transform
        self.transform = get_transform(input_size=224, normalize=True)

        print(f"✅ Fabric classifier ready")

    def classify(self, cv_image, use_feature_enhancement=True):
        """
        Classify fabric type from camera frame.

        Args:
            cv_image: OpenCV image (BGR numpy array)
            use_feature_enhancement: Whether to use texture features

        Returns:
            dict with:
                - fabric_type: Fabric class name
                - confidence: Confidence percentage (0-100)
                - all_probabilities: Dict of all class probabilities
                - fabric_features: dict (if use_feature_enhancement=True)
        """
        # Preprocess image
        with torch.no_grad():
            tensor = preprocess_for_fabric_classification(cv_image, self.transform)
            tensor = tensor.to(self.device)

            # Run model inference
            prediction = self.model.predict(tensor)

        # Extract fabric features if requested
        fabric_features = None
        if use_feature_enhancement:
            fabric_features = extract_fabric_features(cv_image)

            # Enhance prediction with texture analysis
            prediction = enhance_fabric_classification(prediction, fabric_features)

        result = {
            'fabric_type': prediction['fabric_type'],
            'confidence': prediction['confidence'],
            'all_probabilities': prediction['all_probabilities'],
            'class_idx': prediction['class_idx'],
        }

        if fabric_features is not None:
            result['fabric_features'] = fabric_features
            result['feature_boost_applied'] = prediction.get('feature_boost_applied', False)

        return result

    def classify_batch(self, cv_images):
        """
        Classify fabric types in batch of images (for future optimization).

        Args:
            cv_images: List of OpenCV images

        Returns:
            list of classification results
        """
        results = []
        for img in cv_images:
            result = self.classify(img)
            results.append(result)

        return results

    def get_fabric_classes(self):
        """
        Get list of fabric classes.

        Returns:
            list of fabric class names
        """
        return FABRIC_CLASSES
