from ..settings import TextToActionModelSettings
from .base import BaseTextToActionModel


def create_text_to_action_model(settings: TextToActionModelSettings) -> BaseTextToActionModel:
    raise NotImplementedError
