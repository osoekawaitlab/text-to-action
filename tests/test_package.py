import re

import olt2f


def test_olt2f_has_version() -> None:
    assert re.match(r"\d+\.\d+\.\d+", olt2f.__version__)


def test_olt2f_has_text_to_action_core_settings() -> None:
    assert olt2f.TextToActionCoreSettings == olt2f.settings.TextToActionCoreSettings


def test_olt2f_has_text_to_action_core() -> None:
    assert olt2f.TextToActionCore == olt2f.core.TextToActionCore


def test_olt2f_exports_some_models() -> None:
    assert olt2f.Query == olt2f.models.Query
