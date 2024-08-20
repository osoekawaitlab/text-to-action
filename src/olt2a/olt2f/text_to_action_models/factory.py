from ..settings import ActionGemma9bTextToActionModelSettings, TextToActionModelSettings
from .action_gemma_9b import ActionGemma9bTextToActionModel
from .base import BaseTextToActionModel


def create_text_to_action_model(settings: TextToActionModelSettings) -> BaseTextToActionModel:
    if isinstance(settings, ActionGemma9bTextToActionModelSettings):
        return ActionGemma9bTextToActionModel()
    raise ValueError(f"Unsupported text to action model settings: {settings.__class__.__name__}")
