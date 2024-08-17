from enum import Enum
from typing import Annotated, Dict, List, Literal

from oltl import BaseModel as OltlBaseModel
from oltl import NonEmptyStringMixIn, RegexSubstitutedStringMixIn, TrimmedStringMixIn
from pydantic import Field


class NonEmptyTrimmedString(NonEmptyStringMixIn, TrimmedStringMixIn):
    pass


class NonEmptySingleLineTrimmedString(NonEmptyStringMixIn, RegexSubstitutedStringMixIn):
    @classmethod
    def get_pattern_to_repl_map(cls) -> Dict[str, str]:
        return {
            r"^\s+": "",
            r"\s+$": "",
            r"\s+": " ",
        }


class NonEmptySingleLineUnderscoredTrimmedString(NonEmptySingleLineTrimmedString):
    @classmethod
    def get_pattern_to_repl_map(cls) -> Dict[str, str]:
        return {
            r"^\s+": "",
            r"\s+$": "",
            r"\s+": "_",
        }


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
    """


class ActionName(NonEmptySingleLineUnderscoredTrimmedString):
    r"""
    A string that represents an action name.
    The action name should be a non-empty single line stripped string.

    >>> ActionName.from_str("turn_on_light")
    ActionName('turn_on_light')
    >>> ActionName.from_str("  turn on light  ")
    ActionName('turn_on_light')
    >>> ActionName.from_str("  ")
    Traceback (most recent call last):
     ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for function-after[ActionName(), function-before[_proc_str(), constrained-str]]
      String should have at least 1 character [type=string_too_short, input_value='', input_type=str]
     ...
    >>> ActionName.from_str("\na\nb\n")
    ActionName('a_b')
    >>> ActionName.from_str("a\n\nb")
    ActionName('a_b')
    """


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
    """


class Description(NonEmptyTrimmedString): ...


class ParameterType(str, Enum):
    object = "object"


class BaseParameter(OltlBaseModel):
    type: ParameterType
    name: ParameterName
    description: Description
    additional_properties: bool


class ObjectParameter(BaseParameter):
    type: Literal[ParameterType.object] = ParameterType.object
    properties: Dict[str, BaseParameter]
    required: List[str]


Parameter = Annotated[BaseParameter, Field(discriminator="type")]


class BaseModel(OltlBaseModel):
    pass


class Query(BaseModel):
    pass
