"""Test fixture configs."""

from pydantic import BaseModel, Field

from pydraconf.base_config import PydraConfig


class BaseModelConfig(BaseModel):
    """Base model configuration type."""

    size: int = Field(default=100, description="Model size")
    layers: int = Field(default=2, description="Number of layers")


# Main test configuration
class BaseTestConfig(PydraConfig):
    """Base test configuration."""

    value: int = Field(default=10, description="A test value")
    name: str = Field(default="base", description="Config name")
    model: BaseModelConfig = Field(default_factory=BaseModelConfig, description="Model configuration")


class ChildConfig(BaseTestConfig):
    """Child test configuration (variant of PydraConfig)."""

    value: int = 20
    name: str = "child"


class NestedConfig(BaseModel):
    """Nested configuration for testing."""

    inner_value: int = Field(default=5, description="Inner value")


class ComplexConfig(PydraConfig):
    """Complex configuration with nested fields."""

    top_value: int = Field(default=100, description="Top level value")
    nested: BaseModel = Field(default_factory=NestedConfig, description="Nested config")


class ComplexVariant(ComplexConfig):
    """Variant of complex config."""

    top_value: int = 200
