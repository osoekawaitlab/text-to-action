from pytest import mark

import olt2f


@mark.e2e
def test_olt2f_text_to_action() -> None:
    settings = olt2f.TextToActionCoreSettings(text_to_action_model_settings={"type": "ActionGemma-9B"})
    core = olt2f.TextToActionCore.create(settings=settings)
    query = olt2f.Query(
        instruction="Turn on the light of my room",
        tools=[
            olt2f.Tool(
                name="get_light_id_by_alias",
                description="Get the light id by alias",
                parameters={
                    "type": "object",
                    "properties": {
                        "alias": {
                            "type": "string",
                            "description": "The alias of the light",
                        }
                    },
                    "required": ["alias"],
                    "additional_properties": False,
                },
            ),
            olt2f.Tool(
                name="turn_on_light",
                description="Turn on the light",
                parameters={
                    "type": "object",
                    "properties": {
                        "light_id": {
                            "type": "string",
                            "description": "The id of the light",
                        }
                    },
                    "required": ["light_id"],
                    "additional_properties": False,
                },
            ),
        ],
    )
    action = core(query)
    assert not isinstance(action, olt2f.NoAction)
    assert action.name == "turn_on_light"
    assert action.arguments == {"light_id": olt2f.Action(name="get_light_id_by_alias", arguments={"alias": "my room"})}
