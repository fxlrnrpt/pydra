"""Base training configuration."""

from pydantic import BaseModel, Field

from .model.variants import MediumModel, ModelConfig


class TrainConfig(BaseModel):
    """Training configuration with model selection."""

    epochs: int = Field(default=100, description="Number of training epochs")
    batch_size: int = Field(default=32, description="Training batch size")
    learning_rate: float = Field(default=0.001, description="Learning rate")
    model: ModelConfig = Field(default_factory=MediumModel, description="Model configuration")


class QuickTest(TrainConfig):
    """Quick test configuration for development."""

    epochs: int = 5
    batch_size: int = 8


class FullTraining(TrainConfig):
    """Full training configuration for production."""

    epochs: int = 200
    batch_size: int = 128
