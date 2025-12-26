"""
Preprocessing for fabric classification.
Converts camera frames to model-ready tensors.
"""

import cv2
import numpy as np


def preprocess_for_fabric_classification(cv_image, transform):
    """
    Preprocess camera frame for fabric classification.

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


def extract_fabric_features(cv_image):
    """
    Extract texture features that help distinguish fabric types.

    These features can help differentiate:
    - Denim (coarse texture, visible weave)
    - Knit (smooth, stretchy appearance)
    - Cotton (fine texture)
    - Synthetic (uniform, smooth)

    Args:
        cv_image: OpenCV image (BGR numpy array)

    Returns:
        dict: Texture features relevant to fabric classification
    """
    # Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Texture coarseness (using Laplacian)
    texture_coarseness = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Color uniformity (standard deviation in each channel)
    b, g, r = cv2.split(cv_image)
    color_std = np.mean([np.std(b), np.std(g), np.std(r)])

    # Edge density (weave pattern indicator)
    edges = cv2.Canny(gray, 30, 100)
    edge_density = np.count_nonzero(edges) / (edges.shape[0] * edges.shape[1])

    # Brightness (can indicate fabric finish)
    brightness = np.mean(gray)

    return {
        'texture_coarseness': float(texture_coarseness),
        'color_uniformity': float(color_std),
        'edge_density': float(edge_density),
        'brightness': float(brightness)
    }


def enhance_fabric_classification(ml_prediction, fabric_features):
    """
    Enhance ML prediction with texture features.

    Provides additional confidence boost when features match expected patterns.

    Args:
        ml_prediction: ML model prediction dict
        fabric_features: Fabric texture features dict

    Returns:
        dict: Enhanced prediction
    """
    enhanced = ml_prediction.copy()

    fabric_type = enhanced['fabric_type']

    # Heuristic confidence boosts based on texture features
    boost = 1.0

    if fabric_type == "Denim":
        # Denim typically has high texture coarseness and edge density
        if fabric_features['texture_coarseness'] > 150 and fabric_features['edge_density'] > 0.08:
            boost = 1.05

    elif fabric_type == "Örme":
        # Knit fabrics are typically smoother (lower edge density)
        if fabric_features['edge_density'] < 0.06:
            boost = 1.03

    elif fabric_type == "Sentetik":
        # Synthetic fabrics are often very uniform
        if fabric_features['color_uniformity'] < 20:
            boost = 1.04

    # Apply boost (cap at 99%)
    enhanced['confidence'] = min(enhanced['confidence'] * boost, 99.0)
    enhanced['feature_boost_applied'] = boost > 1.0

    return enhanced
