from typing import Annotated, Any
from pydantic import BeforeValidator
from datetime import datetime, date, time

def _parse_numbers(x: dict) -> int | None:
    if x["number"] is None:
        return None
    return int(x["number"])

Numbers = Annotated[int | None, BeforeValidator(_parse_numbers)]

def _parse_text(x: dict) -> str | None:
    return x["text"]

Text = Annotated[str | None, BeforeValidator(_parse_text)]

ColumnInput = dict[str, Any]

def _parse_item_id(x: ColumnInput) -> int | None:
    return int(x["item_id"])

ItemId = Annotated[int | None, BeforeValidator(_parse_item_id)]

def _parse_status(status: ColumnInput) -> str | None:
    return status["label"]

Status = Annotated[str | None, BeforeValidator(_parse_status)]

def _parse_date(x: ColumnInput) -> datetime | None:
    if x["date"] == "":
        return None
        
    else:
        if x["time"] == "":
            _time = time()
        else:
            _time = time.fromisoformat(x["time"])

        return datetime.combine(
            date.fromisoformat(x["date"]),
            _time
        )

Date = Annotated[datetime | None, BeforeValidator(_parse_date)]

def _parse_board_relation(x: dict) -> list[int]:
    return [int(i) for i in x["linked_item_ids"]]

BoardRelation = Annotated[list[int], BeforeValidator(_parse_board_relation)]

def _parse_people(x: dict) -> list[int]:
    return [int(i["id"]) for i in x["persons_and_teams"]]

People = Annotated[list[int], BeforeValidator(_parse_people)]
