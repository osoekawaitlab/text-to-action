from pytest_mock import MockerFixture

from olt2f import core
from olt2f.settings import TextToActionCoreSettings, TextToActionModelType


def test_core_create(mocker: MockerFixture) -> None:
    create_text_to_action_model = mocker.patch("olt2f.core.create_text_to_action_model")
    settings = TextToActionCoreSettings(text_to_action_model_settings={"type": TextToActionModelType.ACTION_GEMMA_9B})
    actual = core.TextToActionCore.create(settings=settings)
    assert isinstance(actual, core.TextToActionCore)
    assert actual.model == create_text_to_action_model.return_value
    create_text_to_action_model.assert_called_once_with(settings=settings.text_to_action_model_settings)
