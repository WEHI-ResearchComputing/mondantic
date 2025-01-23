import pytest
def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--api-key", help="Monday API Key")
    parser.addoption("--board-id", help="Monday board ID")

@pytest.fixture
def api_key(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--api-key"))

@pytest.fixture
def board_id(request: pytest.FixtureRequest) -> int:
    return int(request.config.getoption("--board-id"))
