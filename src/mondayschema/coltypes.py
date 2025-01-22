from typing import Annotated
from pydantic import BeforeValidator
from datetime import datetime, date, time

def _parse_item_id(item_id: dict) -> int:
    return int(item_id["item_id"])

ItemId = Annotated[int, BeforeValidator(_parse_item_id)]

def _parse_status(status: dict) -> str | None:
    if "label" in status:
        return str(status["label"])
    if status.get("index"):
        return str(status["index"])
    return None

Status = Annotated[str | None, BeforeValidator(_parse_status)]

def _parse_date(x: dict) -> datetime | None:
    if x["date"] is None:
        return None
    return datetime.combine(
        date.fromisoformat(x["date"]/1000),
        time.fromisoformat(x["time"]/1000)
    )

Date = Annotated[datetime | None, BeforeValidator(_parse_date)]

def _parse_board_relation(x: dict) -> list[int]:
    return [int(i["linkedPulseId"]) for i in x["linkedPulseIds"]]

BoardRelation = Annotated[list[int], BeforeValidator(_parse_board_relation)]

def _parse_people(x: dict) -> list[int]:
    return [int(i["id"]) for i in x["personsAndTeams"]]

People = Annotated[list[int], BeforeValidator(_parse_people)]
