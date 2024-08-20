from abc import ABC, abstractmethod

from ..models import ActionResult, Query


class BaseTextToActionModel(ABC):
    @abstractmethod
    def __call__(self, query: Query) -> ActionResult:
        raise NotImplementedError
