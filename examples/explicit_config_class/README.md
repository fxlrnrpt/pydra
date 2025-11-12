# Explicit Config Class Example

This example demonstrates how to use the `config_cls` parameter in `@provide_config` to create multiple entry points with different default configurations.

## Use Case

The `config_cls` parameter is useful when you want to:

1. **Force specific defaults** for different environments (dev vs prod)
2. **Create multiple entry points** with different configurations
3. **Simplify deployment** by ensuring production always uses production config

## How It Works

Instead of selecting a config variant via CLI (`--config=QuickTest`), you can specify it directly in the decorator:

```python
@provide_config(config_cls=QuickTest)
def train_dev(cfg: TrainConfig):
    # Will always use QuickTest unless overridden
    ...

@provide_config(config_cls=Production)
def train_prod(cfg: TrainConfig):
    # Will always use Production unless overridden
    ...
```

## Running the Example

```bash
# Development mode (uses QuickTest: 5 epochs, batch_size=16)
python train.py train-dev

# Production mode (uses Production: 200 epochs, batch_size=128)
python train.py train-prod

# Custom mode (uses base config or --config parameter)
python train.py train-custom --config=QuickTest
```

## CLI Overrides Still Work

Even with explicit `config_cls`, you can still override individual fields:

```bash
# Dev mode with custom epoch count
python train.py train-dev --epochs=10

# Production mode with larger batch size
python train.py train-prod --batch_size=256

# Override multiple fields
python train.py train-prod --epochs=300 --learning_rate=0.00005
```

## Benefits

1. **Safety**: Production deployments can't accidentally use test configs
2. **Convenience**: Developers don't need to remember `--config` flags
3. **Flexibility**: Individual fields can still be overridden when needed
4. **Clear Intent**: Each entry point's purpose is explicit in code

## File Structure

```
explicit_config_class/
├── configs/
│   └── base.py          # TrainConfig, QuickTest, Production
├── train.py             # Multiple entry points
└── README.md            # This file
```
