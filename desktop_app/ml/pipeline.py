"""
Textile Inspection ML Pipeline.

Coordinates defect detection and fabric classification.
Main interface for camera manager to use ML system.

PRODUCTION SYSTEM - REAL DEEP LEARNING
Uses PyTorch models for both defect detection and fabric classification.
"""

import torch
import time
from .defect_detection import DefectDetector
from .fabric_classification import FabricClassifier
from .shared.utils import get_device


class TextileInspectionPipeline:
    """
    Complete ML pipeline for textile inspection.

    Performs:
    1. Fabric type classification
    2. Defect detection
    3. Result aggregation

    Both models run in parallel on the same frame.
    """

    def __init__(
        self,
        defect_weights_path=None,
        fabric_weights_path=None,
        device=None,
        confidence_threshold=0.6
    ):
        """
        Initialize ML pipeline.

        Args:
            defect_weights_path: Path to defect detection weights (None = pretrained)
            fabric_weights_path: Path to fabric classification weights (None = pretrained)
            device: torch.device (None = auto-detect)
            confidence_threshold: Minimum confidence for defect reporting (0.0-1.0)
        """
        print("="*60)
        print("INITIALIZING TEXTILE INSPECTION ML PIPELINE")
        print("="*60)

        # Get device
        if device is None:
            device = get_device()
        self.device = device
        print(f"🖥️  Device: {device}")

        # Initialize defect detector
        print("\n1️⃣  DEFECT DETECTION MODULE")
        print("-" * 60)
        try:
            self.defect_detector = DefectDetector(
                weights_path=defect_weights_path,
                device=device,
                confidence_threshold=confidence_threshold
            )
            self.defect_detection_available = True
        except Exception as e:
            print(f"❌ Failed to load defect detector: {e}")
            self.defect_detection_available = False
            raise

        # Initialize fabric classifier
        print("\n2️⃣  FABRIC CLASSIFICATION MODULE")
        print("-" * 60)
        try:
            self.fabric_classifier = FabricClassifier(
                weights_path=fabric_weights_path,
                device=device
            )
            self.fabric_classification_available = True
        except Exception as e:
            print(f"❌ Failed to load fabric classifier: {e}")
            self.fabric_classification_available = False
            raise

        print("\n" + "="*60)
        print("✅ ML PIPELINE READY")
        print("="*60)
        print(f"Defect Classes: {self.defect_detector.get_defect_classes()}")
        print(f"Fabric Classes: {self.fabric_classifier.get_fabric_classes()}")
        print("="*60 + "\n")

        # Performance tracking
        self.total_frames = 0
        self.total_inference_time = 0.0

    def inspect_frame(self, cv_image):
        """
        Perform complete inspection on camera frame.

        Args:
            cv_image: OpenCV image (BGR numpy array)

        Returns:
            dict with:
                - defect_detected: Boolean
                - defect_type: Defect class name or "Temiz"
                - defect_confidence: Confidence percentage (0-100)
                - is_structural: Boolean (yırtık/delik)
                - severity: "HIGH", "MEDIUM", "LOW", "NONE"
                - fabric_type: Fabric class name
                - fabric_confidence: Confidence percentage (0-100)
                - inference_time_ms: Inference time in milliseconds
        """
        start_time = time.time()

        # Run defect detection
        defect_result = self.defect_detector.detect(
            cv_image,
            use_texture_enhancement=True
        )

        # Run fabric classification
        fabric_result = self.fabric_classifier.classify(
            cv_image,
            use_feature_enhancement=True
        )

        # Calculate inference time
        inference_time = (time.time() - start_time) * 1000  # ms

        # Update performance tracking
        self.total_frames += 1
        self.total_inference_time += inference_time

        # Aggregate results
        result = {
            # Defect detection
            'defect_detected': defect_result['defect_detected'],
            'defect_type': defect_result['defect_type'],
            'defect_confidence': defect_result['confidence'],
            'is_structural': defect_result['is_structural'],
            'severity': defect_result['severity'],

            # Fabric classification
            'fabric_type': fabric_result['fabric_type'],
            'fabric_confidence': fabric_result['confidence'],

            # Performance
            'inference_time_ms': inference_time,

            # Additional details (for debugging/analysis)
            'texture_features': defect_result.get('texture_features', {}),
            'fabric_features': fabric_result.get('fabric_features', {}),
            'all_fabric_probabilities': fabric_result.get('all_probabilities', {}),
        }

        return result

    def inspect_batch(self, cv_images):
        """
        Perform inspection on batch of frames.

        Args:
            cv_images: List of OpenCV images

        Returns:
            list of inspection results
        """
        results = []
        for img in cv_images:
            result = self.inspect_frame(img)
            results.append(result)

        return results

    def get_performance_stats(self):
        """
        Get performance statistics.

        Returns:
            dict with performance metrics
        """
        if self.total_frames == 0:
            avg_time = 0.0
        else:
            avg_time = self.total_inference_time / self.total_frames

        return {
            'total_frames_processed': self.total_frames,
            'total_inference_time_ms': self.total_inference_time,
            'average_inference_time_ms': avg_time,
            'estimated_fps': 1000.0 / avg_time if avg_time > 0 else 0.0
        }

    def reset_stats(self):
        """Reset performance statistics."""
        self.total_frames = 0
        self.total_inference_time = 0.0

    def set_confidence_threshold(self, threshold):
        """
        Update defect detection confidence threshold.

        Args:
            threshold: New threshold (0.0-1.0)
        """
        self.defect_detector.set_confidence_threshold(threshold)

    def get_model_info(self):
        """
        Get information about loaded models.

        Returns:
            dict with model information
        """
        return {
            'device': str(self.device),
            'defect_detection_available': self.defect_detection_available,
            'fabric_classification_available': self.fabric_classification_available,
            'defect_classes': self.defect_detector.get_defect_classes(),
            'fabric_classes': self.fabric_classifier.get_fabric_classes(),
            'confidence_threshold': self.defect_detector.confidence_threshold,
        }


def create_ml_pipeline(
    defect_weights=None,
    fabric_weights=None,
    device=None,
    confidence_threshold=0.6
):
    """
    Factory function to create ML pipeline.

    Args:
        defect_weights: Path to defect detection weights
        fabric_weights: Path to fabric classification weights
        device: torch.device or str
        confidence_threshold: Defect detection threshold

    Returns:
        TextileInspectionPipeline instance

    Raises:
        RuntimeError: If models fail to load
    """
    try:
        pipeline = TextileInspectionPipeline(
            defect_weights_path=defect_weights,
            fabric_weights_path=fabric_weights,
            device=device,
            confidence_threshold=confidence_threshold
        )
        return pipeline

    except Exception as e:
        print(f"\n❌ FAILED TO CREATE ML PIPELINE: {e}\n")
        raise RuntimeError(
            f"ML Pipeline initialization failed: {e}\n\n"
            "POSSIBLE CAUSES:\n"
            "1. PyTorch not installed: pip install torch torchvision\n"
            "2. Model weights not found (using pretrained as fallback)\n"
            "3. Insufficient memory\n"
            "4. CUDA not available (will use CPU)\n"
        )
