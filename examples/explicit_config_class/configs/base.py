"""Configuration for the explicit config class example."""

from pydantic import Field

from pydraconf import PydraConfig


class TrainConfig(PydraConfig):
    """Main training configuration."""

    epochs: int = Field(default=100, description="Number of training epochs")
    batch_size: int = Field(default=32, description="Batch size")
    learning_rate: float = Field(default=0.001, description="Learning rate")
    data_path: str = Field(default="./data", description="Path to training data")


class QuickTest(TrainConfig):
    """Quick test configuration - runs fast for development."""

    epochs: int = 5
    batch_size: int = 16


class Production(TrainConfig):
    """Production configuration - full training."""

    epochs: int = 200
    batch_size: int = 128
    learning_rate: float = 0.0001
