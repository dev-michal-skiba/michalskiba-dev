import os
from pathlib import Path

import pytest


@pytest.fixture
def test_working_directory() -> Path:
    return Path(os.getcwd())
