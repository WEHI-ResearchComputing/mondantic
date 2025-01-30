import re
from typing import Iterable
# Characters that should be deleted from identifiers, after separators are replaced
INVALID_CHARS = re.compile(r"[^a-zA-Z]+", flags=re.ASCII)

def to_segments(name: str) -> Iterable[str]:
    """
    Splits a string into segments, each of which is a valid Python identifier.
    """
    # return (INVALID_CHARS.sub(segment, "") for segment in SEPARATOR_CHARS.split(name))
    return (segment for segment in INVALID_CHARS.split(name) if segment)

def clean_class_name(name: str) -> str:
    """
    Cleans a string to be a valid Python class name.
    """
    return "".join([segment.title() for segment in to_segments(name)])

def clean_field_name(name: str) -> str:
    """
    Cleans a string to be a valid Python class name.
    """
    return "_".join([segment.lower() for segment in to_segments(name)])
