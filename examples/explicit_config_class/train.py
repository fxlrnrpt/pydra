"""Example demonstrating explicit config_cls parameter.

This example shows how to use the config_cls parameter to create
multiple entry points with different default configurations.

Usage:
    # Run development training (always uses QuickTest)
    python train.py train-dev

    # Run production training (always uses Production)
    python train.py train-prod

    # Both still support CLI overrides:
    python train.py train-dev --epochs=10
    python train.py train-prod --batch_size=256
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from configs.base import Production, QuickTest, TrainConfig

from pydraconf import provide_config


def train_model(cfg: TrainConfig) -> None:
    """Simulate model training.

    Args:
        cfg: Training configuration
    """
    print("=" * 60)
    print(f"Starting training with {cfg.__class__.__name__}")
    print("=" * 60)
    print("Configuration:")
    print(f"  Epochs:        {cfg.epochs}")
    print(f"  Batch size:    {cfg.batch_size}")
    print(f"  Learning rate: {cfg.learning_rate}")
    print(f"  Data path:     {cfg.data_path}")
    print("=" * 60)
    print(f"\nSimulating {cfg.epochs} epochs of training...")
    print("Training complete!")
    print()


@provide_config(config_cls=QuickTest)
def train_dev(cfg: TrainConfig) -> None:
    """Development entry point - always uses QuickTest config.

    This is perfect for rapid iteration during development.
    You can still override specific fields via CLI if needed.

    Args:
        cfg: Training configuration (will be QuickTest by default)
    """
    print("\n>>> DEVELOPMENT MODE <<<")
    train_model(cfg)


@provide_config(config_cls=Production)
def train_prod(cfg: TrainConfig) -> None:
    """Production entry point - always uses Production config.

    This ensures production runs always use the production configuration
    unless explicitly overridden via CLI.

    Args:
        cfg: Training configuration (will be Production by default)
    """
    print("\n>>> PRODUCTION MODE <<<")
    train_model(cfg)


@provide_config()
def train_custom(cfg: TrainConfig) -> None:
    """Custom entry point - uses base config or --config parameter.

    This follows the standard behavior where you can select any variant
    via the --config CLI parameter.

    Args:
        cfg: Training configuration
    """
    print("\n>>> CUSTOM MODE <<<")
    train_model(cfg)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python train.py train-dev [--OPTIONS]")
        print("  python train.py train-prod [--OPTIONS]")
        print("  python train.py train-custom [--config=VARIANT] [--OPTIONS]")
        print("\nExamples:")
        print("  python train.py train-dev")
        print("  python train.py train-dev --epochs=10")
        print("  python train.py train-prod")
        print("  python train.py train-prod --batch_size=256")
        print("  python train.py train-custom --config=QuickTest")
        print("  python train.py train-custom --config=Production --epochs=300")
        sys.exit(1)

    # Remove the command from argv before calling the function
    command = sys.argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    if command == "train-dev":
        train_dev()
    elif command == "train-prod":
        train_prod()
    elif command == "train-custom":
        train_custom()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: train-dev, train-prod, train-custom")
        sys.exit(1)
