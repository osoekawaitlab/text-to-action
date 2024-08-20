import re

import olt2a


def test_olt2a_has_version() -> None:
    assert re.match(r"\d+\.\d+\.\d+", olt2a.__version__)


def test_olt2a_has_text_to_action_core_settings() -> None:
    assert olt2a.TextToActionCoreSettings == olt2a.settings.TextToActionCoreSettings


def test_olt2a_has_text_to_action_core() -> None:
    assert olt2a.TextToActionCore == olt2a.core.TextToActionCore


def test_olt2a_exports_some_models() -> None:
    assert olt2a.Query == olt2a.models.Query
    assert olt2a.Action == olt2a.models.Action
    assert olt2a.NoAction == olt2a.models.NoAction
    assert olt2a.Tool == olt2a.models.Tool
