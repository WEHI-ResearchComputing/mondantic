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
                          id
                          type
                          value
                          text
                          ... on BoardRelationValue {
                            linked_item_ids
                            display_value
                          },
                          ... on DateValue {
                            time
                            date
                          }
                          ... on StatusValue {
                            label
                          }
                          ... on PeopleValue {
                            persons_and_teams {
                              id
                            }
                          }
                          ... on ItemIdValue {
                            item_id
                          }
                          ... on NumbersValue {
                            number
                          }
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
    res.raise_for_status()
    parsed = res.json()
    for row in parsed["data"]["boards"][0]["items_page"]["items"]:
        model_json = { col["id"]: col for col in row["column_values"] }
        yield cls.model_validate(model_json)
