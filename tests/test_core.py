from pytest_mock import MockerFixture

from olt2a import core
from olt2a.models import Query, Tool
from olt2a.settings import TextToActionCoreSettings, TextToActionModelType
from olt2a.text_to_action_models.base import BaseTextToActionModel


def test_core_create(mocker: MockerFixture) -> None:
    create_text_to_action_model = mocker.patch("olt2a.core.create_text_to_action_model")
    settings = TextToActionCoreSettings(text_to_action_model_settings={"type": TextToActionModelType.ACTION_GEMMA_9B})
    actual = core.TextToActionCore.create(settings=settings)
    assert isinstance(actual, core.TextToActionCore)
    assert actual.model == create_text_to_action_model.return_value
    create_text_to_action_model.assert_called_once_with(settings=settings.text_to_action_model_settings)


def test_core_call(mocker: MockerFixture) -> None:
    model = mocker.Mock(spec=BaseTextToActionModel)
    sut = core.TextToActionCore(model=model)
    query = Query(
        instruction="instruction",
        tools=[Tool(name="name", description="description", parameters={"arg": {"type": "string"}})],
    )
    actual = sut(query=query)
    assert actual == model.return_value
    model.assert_called_once_with(query=query)
