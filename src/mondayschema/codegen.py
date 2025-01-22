from typing import Annotated
import requests
import typer
import ast

TYPE_MAP = {
    "numbers": "int",
    "people": "People",
    "item_id": "ItemId",
    "status": "Status",
    "date": "Date",
    "board_relation": "BoardRelation"
}

def codegen(
    board_id: int,
    api_key: str,
) -> ast.Module:
    """
    Generate a Pydantic model representing a single row of a Monday.com board
    """
    res = requests.post(
        "https://api.monday.com/v2",
        json={
            "query": """
                query($board_id:ID!) {
                    boards(ids:[$board_id]) {
                        name
                        columns {
                            title
                            id
                            type
                        }
                    }
                }
            """,
            "variables": {"board_id": board_id},
        },
        headers={"Authorization": api_key, "API-Version": "2023-04"},
    )
    parsed = res.json()
    columns: list[ast.AnnAssign] = [
        ast.AnnAssign(
            target=ast.Name("board_name"),
            annotation=ast.Subscript(
                value=ast.Name("ClassVar"),
                slice=ast.Name("str"),
            ),
            value=ast.Constant(parsed["data"]["boards"][0]["name"]),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name("board_id"),
            annotation=ast.Subscript(
                value=ast.Name("ClassVar"),
                slice=ast.Name("str"),
            ),
            value=ast.Constant(str(board_id)),
            simple=1,
        )
    ]
    for column in parsed["data"]["boards"][0]["columns"]:
        col_name = column["title"].lower().replace(" ", "_").replace("#", "num").replace("&", "").replace("/", "")
        col_type: str = TYPE_MAP.get(column["type"], "str")
        columns.append(
            ast.AnnAssign(
                target=ast.Name(col_name),
                annotation=ast.Subscript(ast.Name("Optional"), slice=ast.Name(col_type)),
                value=ast.Call(ast.Name("Field"), [], [
                    ast.keyword("alias", ast.Constant(column["id"])),
                    ast.keyword("default", ast.Constant(None)),
                ]),
                # annotation=ast.Subscript(
                #     ast.Name("Annotated"),
                #     slice=ast.Tuple([
                #         ast.Name(col_type),
                #         ast.Call(ast.Name("MondayColumn"), [], [
                #             ast.keyword("name", ast.Constant(column["title"])),
                #             ast.keyword("id", ast.Constant(column["id"])),
                #         ])
                #     ])
                # ),
                simple=1,
            )
        )
    return ast.fix_missing_locations(
        ast.Module(
            body=[
                ast.ImportFrom("mondayschema.coltypes", [
                    ast.alias("ItemId"),
                    ast.alias("People"),
                    ast.alias("Status"),
                    ast.alias("Date"),
                    ast.alias("BoardRelation"),
                ], 0),
                ast.ImportFrom("pydantic", [ast.alias("BaseModel"), ast.alias("Field")], 0),
                ast.ImportFrom("typing", [ast.alias("ClassVar"), ast.alias("Optional")], 0),
                ast.ClassDef(
                    name=parsed["data"]["boards"][0]["name"],
                    bases=[ast.Name("BaseModel", 0)],
                    keywords=[],
                    body=columns,
                    decorator_list=[],
                    type_params=[],
                ),
            ],
            type_ignores=[],
        )
    )


def main(
    board_id: Annotated[
        int,
        typer.Option(
            help="ID of the board to generate code for. This is the last segment of the URL when you open that board."
        ),
    ],
    api_key: Annotated[
        str,
        typer.Option(
            help="API key for the Monday.com API. You can get this from your account settings at https://<YOUR MONDAY INSTANCE>.monday.com/apps/manage/tokens"
        ),
    ],
):
    result = codegen(board_id, api_key)
    print(ast.unparse(result))


if __name__ == "__main__":
    result = typer.run(main)
