from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional, Union

from oltl import BaseModel as OltlBaseModel
from oltl import NonEmptyStringMixIn, RegexSubstitutedStringMixIn, TrimmedStringMixIn
from pydantic import Field


class BaseModel(OltlBaseModel):
    pass


class NonEmptyTrimmedString(NonEmptyStringMixIn, TrimmedStringMixIn):
    pass


class NonEmptySingleLineTrimmedString(NonEmptyStringMixIn, RegexSubstitutedStringMixIn):
    @classmethod
    def get_filling_character(cls) -> str:
        return " "

    @classmethod
    def get_pattern_to_repl_map(cls) -> Dict[str, str]:
        return {
            r"^\s+": "",
            r"\s+$": "",
            r"\s+": cls.get_filling_character(),
        }


class NonEmptySingleLineUnderscoredTrimmedString(NonEmptySingleLineTrimmedString):
    @classmethod
    def get_filling_character(cls) -> str:
        return "_"


class Instruction(NonEmptySingleLineTrimmedString):
    r"""
    A string that represents an instruction.
    The instruction should be a non-empty single line stripped string.

    >>> Instruction.from_str("Turn on the light of my room")
    Instruction('Turn on the light of my room')
    >>> Instruction.from_str("  Turn on the light of my room  ")
    Instruction('Turn on the light of my room')
    >>> Instruction.from_str("  ")
    Traceback (most recent call last):
     ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for function-after[Instruction(), function-before[_proc_str(), constrained-str]]
      String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
     ...
    >>> Instruction.from_str("\na\nb\n")
    Instruction('a b')
    >>> Instruction.from_str("a\n\nb")
    Instruction('a b')
    """  # noqa: E501


class ToolName(NonEmptySingleLineUnderscoredTrimmedString):
    r"""
    A string that represents an action name.
    The action name should be a non-empty single line stripped string.

    >>> ToolName.from_str("turn_on_light")
    ToolName('turn_on_light')
    >>> ToolName.from_str("  turn on light  ")
    ToolName('turn_on_light')
    >>> ToolName.from_str("  ")
    Traceback (most recent call last):
     ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for function-after[ToolName(), function-before[_proc_str(), constrained-str]]
      String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
     ...
    >>> ToolName.from_str("\na\nb\n")
    ToolName('a_b')
    >>> ToolName.from_str("a\n\nb")
    ToolName('a_b')
    """  # noqa: E501


class ParameterName(NonEmptySingleLineUnderscoredTrimmedString):
    r"""
    A string that represents a parameter name.
    The parameter name should be a non-empty single line stripped string.

    >>> ParameterName.from_str("light_id")
    ParameterName('light_id')
    >>> ParameterName.from_str("  light id  ")
    ParameterName('light_id')
    >>> ParameterName.from_str("  ")
    Traceback (most recent call last):
     ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for function-after[ParameterName(), function-before[_proc_str(), constrained-str]]
      String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
     ...
    >>> ParameterName.from_str("\na\nb\n")
    ParameterName('a_b')
    >>> ParameterName.from_str("a\n\nb")
    ParameterName('a_b')
    """  # noqa: E501


class PropertyName(NonEmptySingleLineUnderscoredTrimmedString):
    pass


class Description(NonEmptyTrimmedString):
    r""" """


class ParameterType(str, Enum):
    OBJECT = "object"
    STRING = "string"


class BaseParameter(BaseModel):
    type: ParameterType
    description: Optional[Description] = None


class ObjectParameter(BaseParameter):
    type: Literal[ParameterType.OBJECT] = ParameterType.OBJECT
    properties: Dict[ParameterName, "Parameter"]
    required: List[ParameterName]
    additional_properties: bool


class StringParameter(BaseParameter):
    type: Literal[ParameterType.STRING] = ParameterType.STRING


Parameter = Annotated[Union[ObjectParameter, StringParameter], Field(discriminator="type")]


class Tool(BaseModel):
    name: ToolName
    description: Description
    parameters: Parameter


class Query(BaseModel):
    instruction: Instruction
    tools: List[Tool]


class ActionType(str, Enum):
    NO_ACTION = "no_action"
    ACTION = "action"


class BaseAction(BaseModel):
    type: ActionType


class NoAction(BaseAction):
    type: Literal[ActionType.NO_ACTION] = ActionType.NO_ACTION


class Action(BaseAction):
    type: Literal[ActionType.ACTION] = ActionType.ACTION
    name: ToolName
    arguments: Dict[ParameterName, Union[str, "Action"]]


ActionResult = Annotated[Union[NoAction, Action], Field(discriminator="type")]
