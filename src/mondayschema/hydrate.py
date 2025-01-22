import json
from pydantic import BaseModel
from typing import Iterable, Type
import requests


def hydrate[T: BaseModel](cls: Type[T], api_key: str) -> Iterable[T]:
    """
    Yields instances of the given Pydantic model from the Monday.com API.
    The board's ID is obtained from the model's class attribute `board_id`.
    """
    res = requests.post(
        "https://api.monday.com/v2",
        json={
            "query": """
              query($board_id:ID!) {
                  boards(ids:[$board_id]) {
                    items_page {
                      items {
                        column_values {
                          id,
                          type,
                          value,
                          text
                      }
                    }
                  }
                }
              }
          """,
            "variables": {"board_id": cls.board_id},
        },
        headers={"Authorization": api_key, "API-Version": "2023-04"},
    )
    parsed = res.json()
    for row in parsed["data"]["boards"][0]["items_page"]["items"]:
        model_json = {
            col["id"]: json.loads(col["value"])
            for col in row["column_values"]
            if col["value"] is not None
        }
        model_json = {
            key: value
            for key, value in model_json.items()
            if value is not None and value != {}
        }
        yield cls.model_validate(model_json)
