from pytest import mark

from olt2a.models import Query, Tool
from olt2a.text_to_action_models.action_gemma_9b import ActionGemma9bTextToActionModel


@mark.slow
def test_action_gemma_9b_call() -> None:
    sut = ActionGemma9bTextToActionModel()
    query = Query(
        instruction="Turn on the light of my room",
        tools=[
            Tool(
                name="turn_on_light_by_alias",
                description="Turn on the light by alias",
                parameters={
                    "alias": {
                        "type": "string",
                        "description": "The alias of the light",
                        "enum": ["my_room", "my_kitchen", "my_bathroom"],
                    }
                },
            ),
        ],
    )
    actual = sut(query=query)
    assert actual.name == "turn_on_light_by_alias"
    assert actual.arguments == {"alias": "my_room"}
