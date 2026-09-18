"""
Model Adapter Package for AI Agents
"""

from .model_adapter import (
    CustomModelAdapter,
    AsyncCustomModelAdapter,
    create_default_adapter,
    get_openai_client,
    get_semantic_kernel_config,
    get_autogen_config,
)

__version__ = "1.0.0"
__author__ = "AI Agents for Beginners"
__all__ = [
    "CustomModelAdapter",
    "AsyncCustomModelAdapter", 
    "create_default_adapter",
    "get_openai_client",
    "get_semantic_kernel_config",
    "get_autogen_config",
]