import ast
from mondantic.codegen import codegen
from mondantic.hydrate import hydrate

def test_codegen(api_key: str, board_id: int):
    # Codegen
    result = codegen(board_id, api_key)
    code = compile(ast.unparse(result), "<string>", "exec")
    exec(code, globals(), globals())
    cls = globals()["Batches"]

    # Hydration
    batches = list(hydrate(cls, api_key))
    print(batches)
