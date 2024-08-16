from enum import Enum
from typing import Annotated, Literal

from oltl.settings import BaseSettings as OltlBaseSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict


class BaseSettings(OltlBaseSettings):
    model_config = SettingsConfigDict(env_prefix="OLT2F_")


class TextToActionModelType(str, Enum):
    ACTION_GEMMA_9B = "ActionGemma-9B"


class BaseTextToActionModelSettings(BaseSettings):
    type: TextToActionModelType


class ActionGemma9BTextToActionModelSettings(BaseTextToActionModelSettings):
    type: Literal[TextToActionModelType.ACTION_GEMMA_9B] = TextToActionModelType.ACTION_GEMMA_9B


TextToActionModelSettings = Annotated[ActionGemma9BTextToActionModelSettings, Field(discriminator="type")]


class TextToActionCoreSettings(BaseSettings):
    text_to_action_model_settings: TextToActionModelSettings
