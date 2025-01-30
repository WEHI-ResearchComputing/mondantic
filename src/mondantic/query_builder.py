"""
Utilities for building the mega query that fetches all data from a board
"""
from io import StringIO
from pydantic import BaseModel
from typing import Collection, Type, Union, get_origin
from inspect import isclass, getmembers
from mondantic import schema

def model_to_query(cls: Type[BaseModel], indent: int = 0, exclude: Collection[str] = []) -> str:
    """
    Generates a GraphQL query string that fetches all the fields of the given Pydantic model.
    """
    ret = StringIO()
    ret.write("  " * indent)
    ret.write("{\n")
    for field_name, field in cls.model_fields.items():
      if field_name in exclude:
          continue
      ret.write("  " * (indent + 2))
      ret.write(field_name)
      annotation = field.annotation
      if get_origin(field.annotation) is Union:
        for union_elt in field.annotation.__args__:
          if isclass(union_elt) and issubclass(union_elt, BaseModel):
            annotation = union_elt
            
      if isclass(annotation) and issubclass(annotation, BaseModel):
        ret.write(model_to_query(annotation, indent + 2))

      ret.write("\n")
    ret.write("  " * indent)
    ret.write("}")
    return ret.getvalue()

ALL_VALUE_COLS: list[type[schema.ColumnValue]] = [
   cls for (_name, cls) in getmembers(schema) if isclass(cls) and issubclass(cls, schema.ColumnValue)
]

ALL_VALUE_QUERY = "\n".join([
    f"... on {cls.model_fields['typename__'].default} {model_to_query(cls, exclude=['typename__', 'column'], indent=6)}" for cls in ALL_VALUE_COLS
])

HYDRATE_QUERY = f"""
query($board_id:ID!) {{
    boards(ids:[$board_id]) {{
      items_page {{
      items {{
        column_values {{
{ALL_VALUE_QUERY}
          }}
        }}
      }}
    }}
  }}
"""
