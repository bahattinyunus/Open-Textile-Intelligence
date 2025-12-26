"""
Fabric Classification Model.

PHASE 1 IMPLEMENTATION:
Uses pretrained ResNet-18 with custom classification head.
This is a REAL neural network, not random logic.

IMPORTANT: This is a PLACEHOLDER until a textile-specific model is trained.
"""

import torch
import torch.nn as nn
from torchvision import models


# Fabric type classes
FABRIC_CLASSES = [
    "Pamuk",        # 0 - Cotton
    "Denim",        # 1 - Denim
    "Örme",         # 2 - Knit
    "Dokuma",       # 3 - Woven
    "Sentetik",     # 4 - Synthetic (polyester, nylon, etc.)
]


class FabricClassificationModel(nn.Module):
    """
    Fabric type classification model using pretrained ResNet-18.

    PHASE 1: Pretrained ImageNet features + custom head
    PHASE 2: Replace with textile-specific model trained on fabric dataset

    Architecture:
    - Backbone: ResNet-18 (pretrained on ImageNet)
    - Head: Custom classifier for 5 fabric types
    """

    def __init__(self, num_classes=5, pretrained=True):
        """
        Initialize fabric classification model.

        Args:
            num_classes: Number of fabric types (5)
            pretrained: Whether to use pretrained ImageNet weights
        """
        super(FabricClassificationModel, self).__init__()

        # Load pretrained ResNet-18
        if pretrained:
            weights = models.ResNet18_Weights.IMAGENET1K_V1
            self.backbone = models.resnet18(weights=weights)
        else:
            self.backbone = models.resnet18(weights=None)

        # Get feature dimension
        in_features = self.backbone.fc.in_features

        # Replace final layer with custom classifier
        self.backbone.fc = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, num_classes)
        )

        self.num_classes = num_classes

    def forward(self, x):
        """
        Forward pass.

        Args:
            x: Input tensor (B, 3, H, W)

        Returns:
            logits: Raw class logits (B, num_classes)
        """
        return self.backbone(x)

    def predict(self, x):
        """
        Make prediction with confidence scores.

        Args:
            x: Input tensor (B, 3, H, W)

        Returns:
            dict with:
                - class_idx: Predicted class index
                - fabric_type: Fabric type name
                - confidence: Confidence percentage (0-100)
                - all_probabilities: All class probabilities
        """
        with torch.no_grad():
            logits = self.forward(x)

            # Apply softmax to get probabilities
            probs = torch.softmax(logits, dim=1)

            # Get prediction
            confidence, class_idx = torch.max(probs, dim=1)

            class_idx = class_idx.item()
            confidence_pct = confidence.item() * 100

            fabric_type = FABRIC_CLASSES[class_idx]

            # Get all probabilities for analysis
            all_probs = {
                FABRIC_CLASSES[i]: probs[0, i].item() * 100
                for i in range(len(FABRIC_CLASSES))
            }

            return {
                'class_idx': class_idx,
                'fabric_type': fabric_type,
                'confidence': confidence_pct,
                'all_probabilities': all_probs,
                'raw_logits': logits.cpu().numpy(),
            }


def load_fabric_model(weights_path=None, device='cpu'):
    """
    Load fabric classification model.

    Args:
        weights_path: Path to custom trained weights (None = use pretrained ImageNet)
        device: torch.device or str

    Returns:
        FabricClassificationModel instance
    """
    model = FabricClassificationModel(pretrained=(weights_path is None))

    if weights_path is not None:
        # Load custom weights if provided
        state_dict = torch.load(weights_path, map_location=device)
        model.load_state_dict(state_dict)
        print(f"✅ Loaded custom fabric classification weights from {weights_path}")
    else:
        # Using pretrained ImageNet weights as placeholder
        print("⚠️ Using pretrained ImageNet weights (PLACEHOLDER)")
        print("   Replace with textile-specific model for production")

    model.to(device)
    model.eval()

    return model
