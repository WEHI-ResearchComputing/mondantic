import ast
from mondantic.codegen import codegen
from mondantic.hydrate import hydrate
from mondantic.query_builder import model_to_query
from mondantic.schema import DateValue
import pytest
import os

def test_graphql_query():
    assert model_to_query(DateValue, exclude=["typename__"]).replace(" ", "").replace("\n", "") == """
{
    board_id
    column {
        archived
        description
        id
        settings_str
        title
        type
        width
        typename__
    }
    id
    item_id
    text
    type
    value
    date
    icon
    time
    updated_at
}
    """.replace(" ", "").replace("\n", "")

@pytest.mark.skipif("MONDAY_API_KEY" not in os.environ or "MONDAY_BOARD_ID" not in os.environ, reason="Missing MONDAY_API_KEY or MONDAY_BOARD_ID")
@pytest.mark.skipif("GITHUB_ACTIONS" in os.environ, reason="Skipping in GitHub Actions as it hits the rate limit")
def test_codegen():
    api_key: str = os.environ["MONDAY_API_KEY"]
    board_id: int = int(os.environ["MONDAY_BOARD_ID"])

    # Codegen
    result = codegen(board_id, api_key)
    cls_name = ""
    for stmt in result.body:
        if isinstance(stmt, ast.ClassDef):
            cls_name = stmt.name
    code = compile(ast.unparse(result), "<string>", "exec")
    exec(code, globals(), globals())
    cls = globals()[cls_name]

    # Hydration
    batches = list(hydrate(cls, api_key))
    print(batches)
