"""Logging configuration for PydraConf."""

from __future__ import annotations

import logging
import sys
from typing import Literal

# Global logger for PydraConf
logger = logging.getLogger("pydraconf")
logger.setLevel(logging.INFO)

# Default handler - output to stdout
_default_handler = logging.StreamHandler(sys.stdout)
_default_handler.setFormatter(
    logging.Formatter("%(levelname)s - %(name)s - %(message)s")
)
logger.addHandler(_default_handler)


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def configure_logging(
    level: LogLevel = "INFO",
    *,
    handlers: (
        list[tuple[logging.Handler, str | None]] | logging.Handler | None
    ) = None,
) -> None:
    """
    Configure global logging for PydraConf.

    This function should be called once at the application startup to configure
    how PydraConf logs information.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        handlers: Can be:
            - None: Uses default StreamHandler to stdout with default format
            - Single handler: Uses provided handler with default format
            - List of (handler, format) tuples: Each handler uses its own format (use None for default)

    Example:
        ```python
        import logging
        from pydraconf import configure_logging

        # Basic setup - log to stdout with default format
        configure_logging(level="DEBUG")

        # Single handler with default format
        file_handler = logging.FileHandler("config.log")
        configure_logging(level="INFO", handlers=file_handler)

        # Multiple handlers with different formats
        file_handler = logging.FileHandler("config.log")
        console_handler = logging.StreamHandler()
        configure_logging(
            level="INFO",
            handlers=[
                (file_handler, "%(asctime)s - %(levelname)s - %(message)s"),
                (console_handler, "%(levelname)s - %(message)s"),
            ]
        )

        # Multiple handlers with same custom format
        configure_logging(
            level="INFO",
            handlers=[
                (file_handler, "%(asctime)s - %(levelname)s - %(message)s"),
                (console_handler, "%(asctime)s - %(levelname)s - %(message)s"),
            ]
        )

        # Mix of default and custom formats
        configure_logging(
            level="INFO",
            handlers=[
                (file_handler, None),  # Uses default format
                (console_handler, "%(levelname)s - %(message)s"),  # Custom format
            ]
        )
        ```
    """
    # Clear existing handlers
    logger.handlers.clear()

    # Set log level
    logger.setLevel(getattr(logging, level))

    # Default format
    default_format = "%(levelname)s - %(name)s - %(message)s"

    # Normalize handlers to list of (handler, format) tuples
    handler_format_pairs: list[tuple[logging.Handler, str]] = []

    if handlers is None:
        # Default: stdout with default format
        handler_format_pairs = [(logging.StreamHandler(sys.stdout), default_format)]
    elif isinstance(handlers, logging.Handler):
        # Single handler with default format
        handler_format_pairs = [(handlers, default_format)]
    elif isinstance(handlers, list):
        if not handlers:
            # Empty list, use default
            handler_format_pairs = [(logging.StreamHandler(sys.stdout), default_format)]
        else:
            # List of (handler, format) tuples
            handler_format_pairs = [
                (h, fmt if fmt is not None else default_format)
                for h, fmt in handlers  # type: ignore[misc]
            ]

    # Add all handlers with their formatters
    for handler, fmt in handler_format_pairs:
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
