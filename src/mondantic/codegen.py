from typing import Annotated, Type
import requests
import typer
import ast
import re
from mondantic import schema

INVALID_CHARS = re.compile(r"[^a-zA-Z0-9_]")

TYPE_MAP: dict[str, Type[schema.ColumnValue]] = {
    "mirror": schema.MirrorValue,
    "numbers": schema.NumbersValue,
    "board_relation": schema.BoardRelationValue,
    "button": schema.ButtonValue,
    "checkbox": schema.CheckboxValue,
    "color_picker": schema.ColorPickerValue,
    "country": schema.CountryValue,
    "creation_log": schema.CreationLogValue,
    "date": schema.DateValue,
    "dependency": schema.DependencyValue,
    "doc": schema.DocValue,
    "dropdown": schema.DropdownValue,
    "email": schema.EmailValue,
    "file": schema.FileValue,
    "formula": schema.FormulaValue,
    "hour": schema.HourValue,
    "integration": schema.IntegrationValue,
    # Not sure if this is correct
    "item_assignees": schema.ItemIdValue,
    "item_id": schema.ItemIdValue,
    "last_updated": schema.LastUpdatedValue,
    "link": schema.LinkValue,
    "location": schema.LocationValue,
    "people": schema.PeopleValue,
    "person": schema.PersonValue,
    "phone": schema.PhoneValue,
    "progress": schema.ProgressValue,
    "rating": schema.RatingValue,
    "status": schema.StatusValue,
    "subtasks": schema.SubtasksValue,
    "tags": schema.TagsValue,
    "team": schema.TeamValue,
    "text": schema.TextValue,
    "time_tracking": schema.TimeTrackingValue,
    "timeline": schema.TimelineValue,
    "unsupported": schema.UnsupportedValue,
    "vote": schema.VoteValue,
    "week": schema.WeekValue,
    "world_clock": schema.WorldClockValue,
}
# DEFAULT_MAP: dict[str, ast.expr] = {
#     "people": ast.List([]),
#     "board_relation": ast.List([])
# }

app = typer.Typer()

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
    res.raise_for_status()
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
        col_type: Type[schema.ColumnValue] = TYPE_MAP.get(column["type"], schema.ColumnValue)
        # default: ast.expr = DEFAULT_MAP.get(column["type"], ast.Constant(None))
        columns.append(
            ast.AnnAssign(
                target=ast.Name(col_name),
                # annotation=ast.Name(col_type.__name__),
                annotation=ast.Subscript(ast.Name("Optional"), slice=ast.Name(col_type.__name__)),
                value=ast.Call(ast.Name("Field"), [], [
                    ast.keyword("alias", ast.Constant(column["id"])),
                    ast.keyword("default", ast.Constant(None)),
                ]),
                simple=1,
            )
        )
    
    clean_board_name = INVALID_CHARS.sub("", parsed["data"]["boards"][0]["name"])
    return ast.fix_missing_locations(
        ast.Module(
            body=[
                ast.ImportFrom("mondantic.schema", [
                    ast.Name(cls.__name__) for cls in TYPE_MAP.values()
                ] + [ast.Name("ColumnValue")], 0),
                ast.ImportFrom("pydantic", [ast.alias("BaseModel"), ast.alias("Field")], 0),
                ast.ImportFrom("typing", [ast.alias("ClassVar"), ast.alias("Optional")], 0),
                ast.ClassDef(
                    name=clean_board_name,
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


@app.command()
def cli_codegen(
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


def main():
    app()

if __name__ == "__main__":
    main()
