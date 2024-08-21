import os
from typing import Any, Dict, List, Optional, Union

from torch import Tensor

class PreTrainedTokenizerBase:
    def encode(self, text: str, return_tensors: str) -> Tensor: ...
    def decode(self, ids: List[int], skip_special_tokens: bool) -> str: ...
    def apply_chat_template(
        self, messages: list[dict[str, str]], tokenize: bool, add_generation_prompt: bool
    ) -> str: ...
    def __call__(self, text: str, return_tensors: str) -> Dict[str, Tensor]: ...

class PreTrainedModel:
    def generate(
        self, input_ids: Tensor, attention_mask: Tensor, max_new_tokens: int, do_sample: bool, num_return_sequences: int
    ) -> List[List[int]]: ...
    @property
    def device(self) -> str: ...

class AutoTokenizer:
    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: Union[str, os.PathLike[str]],
        *init_inputs: Any,
        cache_dir: Optional[Union[str, os.PathLike[str]]] = None,
        force_download: bool = False,
        local_files_only: bool = False,
        token: Optional[Union[str, bool]] = None,
        revision: str = "main",
        **kwargs: Any,
    ) -> PreTrainedTokenizerBase: ...

class AutoModelForCausalLM:
    @classmethod
    def from_pretrained(
        cls, pretrained_model_name_or_path: Union[str, os.PathLike[str]], *model_args: Any, **kwargs: Any
    ) -> PreTrainedModel: ...
