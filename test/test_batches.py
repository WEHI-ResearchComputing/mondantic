import ast
from mondantic.codegen import codegen
from mondantic.hydrate import hydrate
from mondantic.query_builder import model_to_query
from mondantic.schema import DateValue

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

def test_codegen(api_key: str, board_id: int):
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
