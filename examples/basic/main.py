"""Basic example demonstrating PydraConf features."""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from configs.base import AppConfig

from pydraconf import provide_config


@provide_config(AppConfig)  # config_dir read from pyproject.toml
def run(cfg: AppConfig) -> None:
    """Run the application with the given config.

    Args:
        cfg: Application configuration
    """
    print("=" * 50)
    print(f"Running {cfg.__class__.__name__}")
    print("=" * 50)
    print(f"Host: {cfg.host}")
    print(f"Port: {cfg.port}")
    print(f"Debug: {cfg.debug}")
    print("=" * 50)


if __name__ == "__main__":
    run()
