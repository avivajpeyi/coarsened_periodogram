import pytest
import os

DIRNAME = os.path.dirname(__file__)
TST_DIR = os.path.join(DIRNAME, "out_tests")


@pytest.fixture
def tmpdir():
    os.makedirs(TST_DIR, exist_ok=True)
    return TST_DIR


@pytest.fixture
def wdb_strain():
    pass
