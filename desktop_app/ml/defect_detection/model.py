"""
Defect Detection Model.

PHASE 1 IMPLEMENTATION:
Uses pretrained EfficientNet-B0 with custom classification head.
This is a REAL neural network, not random logic.

IMPORTANT: This is a PLACEHOLDER until a textile-specific model is trained.
The architecture is designed to be easily replaced with YOLO/segmentation models.
"""

import torch
import torch.nn as nn
from torchvision import models


# Defect classes (index 0 = no defect, 1-6 = defects)
DEFECT_CLASSES = [
    "Temiz",                # 0 - No defect
    "Leke",                 # 1 - Stain
    "Delik",                # 2 - Hole (STRUCTURAL)
    "Yırtık",               # 3 - Tear (STRUCTURAL)
    "İplik Kopması",        # 4 - Thread break
    "Renk Uyumsuzluğu",     # 5 - Color mismatch
    "Dokuma Hatası",        # 6 - Weaving defect
]

# Structural defects (high severity)
STRUCTURAL_DEFECTS = {"Delik", "Yırtık"}


class DefectDetectionModel(nn.Module):
    """
    Defect detection model using pretrained EfficientNet-B0.

    PHASE 1: Pretrained ImageNet features + custom head
    PHASE 2: Replace with textile-specific YOLO/segmentation model

    Architecture:
    - Backbone: EfficientNet-B0 (pretrained on ImageNet)
    - Head: Custom classifier for 7 classes (1 clean + 6 defects)
    """

    def __init__(self, num_classes=7, pretrained=True):
        """
        Initialize defect detection model.

        Args:
            num_classes: Number of classes (7 = 1 clean + 6 defect types)
            pretrained: Whether to use pretrained ImageNet weights
        """
        super(DefectDetectionModel, self).__init__()

        # Load pretrained EfficientNet-B0
        if pretrained:
            # Use weights parameter instead of deprecated pretrained
            weights = models.EfficientNet_B0_Weights.IMAGENET1K_V1
            self.backbone = models.efficientnet_b0(weights=weights)
        else:
            self.backbone = models.efficientnet_b0(weights=None)

        # Get feature dimension
        in_features = self.backbone.classifier[1].in_features

        # Replace classifier head with custom head for defect detection
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=True),
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
                - class_name: Defect class name
                - confidence: Confidence percentage (0-100)
                - is_defective: Boolean
                - is_structural: Boolean (for delik/yırtık)
        """
        with torch.no_grad():
            logits = self.forward(x)

            # Apply softmax to get probabilities
            probs = torch.softmax(logits, dim=1)

            # Get prediction
            confidence, class_idx = torch.max(probs, dim=1)

            class_idx = class_idx.item()
            confidence_pct = confidence.item() * 100

            class_name = DEFECT_CLASSES[class_idx]
            is_defective = class_idx > 0  # Index 0 is "Temiz"
            is_structural = class_name in STRUCTURAL_DEFECTS

            return {
                'class_idx': class_idx,
                'class_name': class_name,
                'confidence': confidence_pct,
                'is_defective': is_defective,
                'is_structural': is_structural,
                'raw_logits': logits.cpu().numpy(),
                'probabilities': probs.cpu().numpy()
            }


def load_defect_model(weights_path=None, device='cpu'):
    """
    Load defect detection model.

    Args:
        weights_path: Path to custom trained weights (None = use pretrained ImageNet)
        device: torch.device or str

    Returns:
        DefectDetectionModel instance
    """
    model = DefectDetectionModel(pretrained=(weights_path is None))

    if weights_path is not None:
        # Load custom weights if provided
        state_dict = torch.load(weights_path, map_location=device)
        model.load_state_dict(state_dict)
        print(f"✅ Loaded custom defect detection weights from {weights_path}")
    else:
        # Using pretrained ImageNet weights as placeholder
        print("⚠️ Using pretrained ImageNet weights (PLACEHOLDER)")
        print("   Replace with textile-specific model for production")

    model.to(device)
    model.eval()

    return model
