"""
Image preprocessing transforms for textile inspection.
Standard transforms compatible with PyTorch pretrained models.
"""

import torch
from torchvision import transforms
import numpy as np


def get_transform(input_size=224, normalize=True):
    """
    Get standard image transform for textile inspection.

    Args:
        input_size: Target image size (default 224 for most pretrained models)
        normalize: Whether to apply ImageNet normalization

    Returns:
        torchvision.transforms.Compose object
    """
    transform_list = [
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
    ]

    if normalize:
        # ImageNet normalization (standard for pretrained models)
        transform_list.append(
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        )

    return transforms.Compose(transform_list)


def get_augmentation_transform(input_size=224):
    """
    Get augmentation transform for training (future use).

    Args:
        input_size: Target image size

    Returns:
        torchvision.transforms.Compose object
    """
    return transforms.Compose([
        transforms.RandomResizedCrop(input_size),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def opencv_to_pil(cv_image):
    """
    Convert OpenCV BGR image to PIL RGB image.

    Args:
        cv_image: OpenCV image (BGR, numpy array)

    Returns:
        PIL Image (RGB)
    """
    from PIL import Image
    import cv2

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    # Convert to PIL
    pil_image = Image.fromarray(rgb_image)

    return pil_image
