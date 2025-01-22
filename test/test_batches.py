import ast
from mondayschema.codegen import codegen
from mondayschema.hydrate import hydrate

def test_codegen(api_key: str, board_id: int):
    # Codegen
    result = codegen(board_id, api_key)
    code = compile(ast.unparse(result), "<string>", "exec")
    exec(code, globals(), globals())
    cls = globals()["Batches"]

    # Hydration
    batches = list(hydrate(cls, api_key))
    print(batches)
