# DbssertAPI

## Version 1.0.0

Simple Python FastAPI service for querying CURIE metadata from a Dbssert DuckDB file.

This repository complements [Dbssert](https://github.com/SkyeAv/Dbssert) and is part of the broader [Tablassert](https://github.com/SkyeAv/Tablassert) ecosystem.

## Usage

Set database path (required)
```bash
export DBSSERT_PATH=/path/to/dbssert.duckdb
```

Install dependencies (Nix shell)
```bash
nix develop
```

Run server
```bash
serve-api
```

Server starts on port `8052`.

## API Routes

Health check endpoint:

```
GET /health
```

Returns plain text `ok`.

Entity lookup endpoint:

```
GET /curies-with-ner?entity=<text>
```

Returns JSON (`application/json`) as a list of records, including:
- `CURIE`
- `PREFERRED_NAME`
- `SYNONYM`
- `CATEGORY_NAME`
- `TAXON_ID`

Canonical CURIE lookup endpoint:

```
GET /cannoical-curie-information?curie=<CURIE>
```

Returns JSON (`application/json`) as a list of records, including:
- `CURIE`
- `PREFERRED_NAME`
- `CATEGORY_NAME`
- `TAXON_ID`

## Architecture

Single-file implementation in `lib/dbssert_api/api.py`:

1. **FastAPI app (`APP`)** - Declares all HTTP routes.
2. **DuckDB query handlers** - Open `DBSSERT_PATH` in read-only mode and query CURIE metadata.
3. **`serve_api()`** - Starts Uvicorn on `0.0.0.0:8052`.

## Development

Enter development shell:

```bash
nix develop
```

Run server locally:

```bash
serve-api
```

## Contributors

[Skye Lane Goetz](mailto:sgoetz@isbscience.org)

[Gwênlyn Glusman](mailto:gglusman@isbscience.org)
