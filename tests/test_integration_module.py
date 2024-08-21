from pytest import mark

import olt2a


@mark.e2e
def test_olt2a_text_to_action() -> None:
    settings = olt2a.TextToActionCoreSettings(text_to_action_model_settings={"type": "ActionGemma-9B"})
    core = olt2a.TextToActionCore.create(settings=settings)
    query = olt2a.Query(
        instruction="Turn on the light of my room",
        tools=[
            olt2a.Tool(
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
    action = core(query)
    assert isinstance(action, olt2a.Action)
    assert action.name == "turn_on_light_by_alias"
    assert action.arguments == {"alias": "my_room"}
