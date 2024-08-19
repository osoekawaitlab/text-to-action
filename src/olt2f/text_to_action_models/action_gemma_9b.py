from ..models import ActionResult, Query
from .base import BaseTextToActionModel


class ActionGemma9bTextToActionModel(BaseTextToActionModel):
    def __call__(self, query: Query) -> ActionResult:
        raise NotImplementedError
