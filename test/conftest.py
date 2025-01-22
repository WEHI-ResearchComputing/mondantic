import pytest
def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--api_key", help="Monday API Key")
    parser.addoption("--board_id", help="Monday board ID")

@pytest.fixture
def api_key(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--api_key"))

@pytest.fixture
def board_id(request: pytest.FixtureRequest) -> int:
    return int(request.config.getoption("--board_id"))
