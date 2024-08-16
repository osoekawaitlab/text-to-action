import pytest

from olt2f.settings import BaseTextToActionModelSettings, TextToActionModelType
from olt2f.text_to_action_models.factory import create_text_to_action_model


def test_create_text_to_action_model_raises_value_error() -> None:
    settings = BaseTextToActionModelSettings(type=TextToActionModelType.ACTION_GEMMA_9B)
    with pytest.raises(ValueError):
        create_text_to_action_model(settings=settings)  # type: ignore[arg-type]
