"""
Preprocessing for defect detection.
Converts camera frames to model-ready tensors.
"""

import cv2
import numpy as np
import torch


def preprocess_for_defect_detection(cv_image, transform):
    """
    Preprocess camera frame for defect detection.

    Args:
        cv_image: OpenCV image (BGR numpy array)
        transform: torchvision transform

    Returns:
        torch.Tensor: Preprocessed image tensor (1, 3, H, W)
    """
    from ..shared.utils import load_image_tensor

    # Convert OpenCV image to tensor
    tensor = load_image_tensor(cv_image, transform)

    return tensor


def extract_texture_features(cv_image):
    """
    Extract texture features for structural defect detection.

    This is used as ADDITIONAL evidence for yırtık/delik detection.
    The main detection is done by the neural network.

    Args:
        cv_image: OpenCV image (BGR numpy array)

    Returns:
        dict: Texture features
            - edge_density: Percentage of edge pixels
            - blur_score: Laplacian variance (higher = sharper)
            - contrast: Standard deviation of pixel intensities
    """
    # Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Edge detection (Canny)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.count_nonzero(edges) / (edges.shape[0] * edges.shape[1])

    # Blur measurement (Laplacian variance)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Contrast measurement
    contrast = np.std(gray)

    return {
        'edge_density': float(edge_density),
        'blur_score': float(blur_score),
        'contrast': float(contrast)
    }


def enhance_defect_detection(ml_prediction, texture_features):
    """
    Enhance ML prediction with texture analysis for structural defects.

    This combines neural network output with classical CV features
    to improve detection of yırtık and delik.

    Args:
        ml_prediction: ML model prediction dict
        texture_features: Texture features dict

    Returns:
        dict: Enhanced prediction with adjusted confidence
    """
    enhanced = ml_prediction.copy()

    # If ML detected structural defect, verify with texture features
    if enhanced['is_structural']:
        # High edge density suggests actual structural damage
        edge_boost = texture_features['edge_density'] > 0.12

        # Low blur suggests clear defect boundary
        sharpness_boost = texture_features['blur_score'] > 80

        # Boost confidence if texture features confirm
        if edge_boost or sharpness_boost:
            enhanced['confidence'] = min(enhanced['confidence'] * 1.1, 99.0)
            enhanced['texture_confirmed'] = True
        else:
            enhanced['texture_confirmed'] = False

    return enhanced
