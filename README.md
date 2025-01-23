# mondantic

Converts from Monday.com boards to Pydantic dataclasses.

## Installation

```bash
pip install git+ssh://git@github.com/WEHI-ResearchComputing/mondantic.git
```

## CLI

The next step is to generate the Pydantic schema:

```bash
mondantic-codegen --board-id $SOME_BOARD --api-key $SOME_KEY > models.py
```

## API

Then, you can create instances of these models in Python:

```python
from models import BoardModel
from mondantic.hydrate import hydrate

for instance in hydrate(BoardModel, api_key):
    # Use instance
```
