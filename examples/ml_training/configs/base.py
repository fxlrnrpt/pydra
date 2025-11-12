"""Base training configuration."""

from pydantic import BaseModel, Field

from pydraconf import PydraConfig


# Base config types for groups (with sane defaults)
# These can still use BaseModel since they're nested configs
class ModelConfig(BaseModel):
    """Base model config type."""

    hidden_dim: int = Field(default=512, description="Hidden dimension size")
    num_layers: int = Field(default=6, description="Number of layers")


class OptimizerConfig(BaseModel):
    """Base optimizer config type."""

    lr: float = Field(default=0.001, description="Learning rate")


# Main config uses PydraConfig for metadata tracking
class TrainConfig(PydraConfig):
    """Main training configuration."""

    epochs: int = Field(default=100, description="Number of training epochs")
    batch_size: int = Field(default=32, description="Training batch size")
    model: ModelConfig = Field(default_factory=ModelConfig, description="Model configuration")
    optimizer: OptimizerConfig = Field(default_factory=OptimizerConfig, description="Optimizer configuration")
    seed: int = Field(default=42, description="Random seed")


class QuickTest(TrainConfig):
    """Quick test configuration variant."""

    epochs: int = 5
    batch_size: int = 8


class FullTraining(TrainConfig):
    """Full training configuration variant."""

    epochs: int = 200
    batch_size: int = 64
