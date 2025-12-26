"""Utility functions for ML pipeline."""

import torch
import numpy as np
from PIL import Image


def load_image_tensor(cv_image, transform):
    """
    Convert OpenCV image to PyTorch tensor.

    Args:
        cv_image: OpenCV image (BGR numpy array)
        transform: torchvision transform to apply

    Returns:
        torch.Tensor: Image tensor ready for model input
    """
    from .transforms import opencv_to_pil

    # Convert to PIL
    pil_image = opencv_to_pil(cv_image)

    # Apply transform
    tensor = transform(pil_image)

    # Add batch dimension
    tensor = tensor.unsqueeze(0)

    return tensor


def tensor_to_numpy(tensor):
    """
    Convert PyTorch tensor to numpy array.

    Args:
        tensor: torch.Tensor

    Returns:
        numpy.ndarray
    """
    return tensor.detach().cpu().numpy()


def get_device():
    """
    Get the best available device (CUDA if available, else CPU).

    Returns:
        torch.device
    """
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')


def calculate_confidence(logits):
    """
    Calculate confidence score from model logits using softmax.

    Args:
        logits: Raw model outputs (torch.Tensor or numpy.ndarray)

    Returns:
        float: Confidence percentage (0-100)
    """
    if isinstance(logits, torch.Tensor):
        logits = tensor_to_numpy(logits)

    # Apply softmax
    exp_logits = np.exp(logits - np.max(logits))
    probabilities = exp_logits / np.sum(exp_logits)

    # Get max probability
    confidence = np.max(probabilities) * 100

    return confidence
