## Docs

Documentation is currently only the readme.
This is built from `README.qmd`, but the right parameters need to be passed in.
e.g. 
```bash
uv run quarto render README.qmd -P 'board:XXX' -P 'api_key:YYYY'
```

## Schema Generation

This updates `schema.py`:
```bash
uv run datamodel-codegen --url 'https://api.monday.com/v2/get_schema?format=sdl'  --input-file-type graphql > src/mondantic/schema.py
```

## Tests

The tests also need an API key and board.
Hence, to run them you do something like:
```bash
uv run pytest test --api-key "XXXXX" --board-id "YYYYYY"
```
