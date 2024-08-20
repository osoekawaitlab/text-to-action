from .models import ActionResult, Query
from .settings import TextToActionCoreSettings
from .text_to_action_models.base import BaseTextToActionModel
from .text_to_action_models.factory import create_text_to_action_model


class TextToActionCore:
    def __init__(self, model: BaseTextToActionModel):
        self._model = model

    @property
    def model(self) -> BaseTextToActionModel:
        return self._model

    @classmethod
    def create(cls, settings: TextToActionCoreSettings) -> "TextToActionCore":
        return cls(model=create_text_to_action_model(settings=settings.text_to_action_model_settings))

    def __call__(self, query: Query) -> ActionResult:
        return self.model(query=query)
