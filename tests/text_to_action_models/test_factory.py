import pytest
from pytest_mock import MockerFixture

from olt2f.settings import (
    ActionGemma9bTextToActionModelSettings,
    BaseTextToActionModelSettings,
    TextToActionModelType,
)
from olt2f.text_to_action_models.factory import create_text_to_action_model


def test_create_text_to_action_model_raises_value_error() -> None:
    settings = BaseTextToActionModelSettings(type=TextToActionModelType.ACTION_GEMMA_9B)
    with pytest.raises(ValueError):
        create_text_to_action_model(settings=settings)  # type: ignore[arg-type]


def test_create_text_to_action_model_creates_action_gemma_9b(mocker: MockerFixture) -> None:
    ActionGemma9bTextToActionModel = mocker.patch("olt2f.text_to_action_models.factory.ActionGemma9bTextToActionModel")
    settings = ActionGemma9bTextToActionModelSettings()
    actual = create_text_to_action_model(settings=settings)
    assert actual == ActionGemma9bTextToActionModel.return_value
    ActionGemma9bTextToActionModel.assert_called_once_with()
