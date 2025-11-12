"""Integration tests for end-to-end config building."""

from pathlib import Path
from typing import cast

from pydraconf.cli import ConfigCLIParser
from pydraconf.decorators import _build_config
from pydraconf.registry import ConfigRegistry
from tests.fixtures.configs.base import BaseModelConfig, BaseTestConfig, ChildConfig
from tests.fixtures.configs.model.small import SmallModelConfig


FIXTURES_PATH = Path(__file__).parent / "fixtures" / "configs"


def build_config_with_args(args: list[str]) -> BaseTestConfig:
    """Helper to build config from CLI args with discovery."""
    registry = ConfigRegistry()
    registry.discover(FIXTURES_PATH, BaseTestConfig)

    parser = ConfigCLIParser(BaseTestConfig, registry)
    variant_name, groups, overrides = parser.parse(args)

    # Determine final class
    if variant_name:
        final_cls = registry.get_variant(variant_name)
    else:
        final_cls = BaseTestConfig

    return _build_config(final_cls, registry, groups, overrides, variant_name, [str(FIXTURES_PATH)])  # type: ignore[return-value]


class TestIntegration:
    """Integration tests for full config building pipeline.

    These tests verify the complete pipeline: discovery -> parsing -> building -> applying overrides.
    Unit tests for individual components (CLI parser, registry, etc.) are in separate test files.
    """

    def test_base_config_only(self):
        """Test building config with no overrides - baseline behavior."""
        config = build_config_with_args([])

        assert isinstance(config, BaseTestConfig)
        assert config.value == 10
        assert isinstance(config.model, BaseModelConfig)
        assert config.model.size == 100

    def test_override_priority(self):
        """Test complete override priority system: CLI > groups > variant > base.

        This comprehensive test validates:
        - Variant selection (--config=ChildConfig)
        - Group selection (model=SmallModelConfig)
        - Field overrides (--value=15)
        - Nested field overrides (--model.layers=5)
        - Correct priority order

        Priority breakdown:
        - Base: value=10, model.size=100, model.layers=2
        - Variant (ChildConfig): value=20
        - Group (SmallModelConfig): model.size=50, model.layers=1
        - CLI: value=15, model.layers=5

        Expected result:
        - value=15 (CLI overrides variant)
        - model.size=50 (from group)
        - model.layers=5 (CLI overrides group)
        """
        config = cast(
            ChildConfig,
            build_config_with_args(["--config=ChildConfig", "model=SmallModelConfig", "--value=15", "--model.layers=5"]),
        )

        # Verify correct config type (variant selection)
        assert isinstance(config, ChildConfig)

        # Verify CLI override has highest priority (overrides variant default of 20)
        assert config.value == 15

        # Verify group selection works
        assert config.model.__class__.__name__ == "SmallModelConfig"
        assert isinstance(config.model, SmallModelConfig)

        # Verify group default is used (from SmallModelConfig)
        assert config.model.size == 50

        # Verify CLI override has highest priority (overrides group default of 1)
        assert config.model.layers == 5  # pyright: ignore[reportAttributeAccessIssue]
