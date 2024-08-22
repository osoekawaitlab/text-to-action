import json
from typing import Any, Dict, List

from oltl import JsonAcceptable
from pydantic import TypeAdapter
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from ..models import Action, ActionResult, BaseModel, NoAction, Query, Tool
from .base import BaseTextToActionModel


class ActionGemma9bAction(BaseModel):
    name: str
    arguments: Dict[str, Any]


ActionGemma9bActions = List[ActionGemma9bAction]

ActionGemma9bResultModel = TypeAdapter(ActionGemma9bActions)


class ActionGemma9bTextToActionModel(BaseTextToActionModel):
    def __init__(self) -> None:
        self._tokenizer: PreTrainedTokenizerBase | None = None
        self._model: PreTrainedModel | None = None

    @property
    def tokenizer(self) -> PreTrainedTokenizerBase:
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained("KishoreK/ActionGemma-9B")
        return self._tokenizer

    @property
    def model(self) -> PreTrainedModel:
        if self._model is None:
            self._model = AutoModelForCausalLM.from_pretrained("KishoreK/ActionGemma-9B", use_cache=True)
        return self._model

    @staticmethod
    def _format_tools(tools: List[Tool]) -> List[Dict[str, JsonAcceptable]]:
        return [ActionGemma9bTextToActionModel._format_tool(tool) for tool in tools] + [
            ActionGemma9bTextToActionModel._format_tool(
                Tool(
                    name="no_action",
                    description="Select this whenever all other tools seems to be wrong",
                    parameters={
                        "reason": {
                            "type": "string",
                            "description": "The reason why no other tools can be used",
                        }
                    },
                )
            )
        ]

    @staticmethod
    def _format_tool(tool: Tool) -> Dict[str, JsonAcceptable]:
        return tool.model_dump()

    def __call__(self, query: Query) -> ActionResult:
        messages = self.tokenizer.apply_chat_template(
            [
                {
                    "role": "system",
                    "content": """\
You are an expert in composing functions. \
You are given a question and a set of possible functions. \
Based on the question, you will need to make one or more function/tool calls to achieve the purpose. \
If none of the functions can be used, point it out and refuse to answer. \
If the given question lacks the parameters required by the function, also point it out.""",
                },
                {"role": "user", "content": query.instruction},
                {"role": "tools", "content": json.dumps(self._format_tools(query.tools))},
            ],
            add_generation_prompt=True,
            tokenize=False,
        )
        inputs = self.tokenizer(messages, return_tensors="pt")
        outputs = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=512,
            do_sample=False,
            num_return_sequences=1,
        )
        result = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True)
        try:
            action = ActionGemma9bResultModel.validate_json(result)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode the result: {result}")
        if action[0].name == "no_action":
            return NoAction(comment=action[0].arguments["reason"])
        return Action(name=action[0].name, arguments=action[0].arguments)
