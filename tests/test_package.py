import re

import olt2f


def test_olt2f_has_version() -> None:
    assert re.match(r"\d+\.\d+\.\d+", olt2f.__version__)
