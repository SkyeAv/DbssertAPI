from fastapi import FastAPI
from typing import Any
from os import environ as env
import uvicorn
import json
import duckdb
import polars as pl

APP: Any = FastAPI()
DBSSERT_PATH: str = env["DBSSERT_PATH"]

@APP.get("/curies-with-ner")
def get_curies_with_ner(entity: str) -> str:
  p: str = DBSSERT_PATH
  with duckdb.connect(p, read_only=True) as conn:
    entity = entity.lower()
    sql: str = f"SELECT * FROM SYNONYMS S JOIN CURIES C ON S.CURIE_ID = C.CURIE_ID WHERE S.SYNONYM = '{entity}' LIMIT 10;"
    df: pl.DataFrame = conn.sql(sql).pl()
    return json.dumps(df.to_dicts())

@APP.get("/cannoical-curie-information")
def get_cannoical_curie_information(curie: str) -> str:
  p: str = DBSSERT_PATH
  with duckdb.connect(p, read_only=True) as conn:
    sql: str = f"SELECT * FROM CURIES C WHERE C.CURIE = '{curie}' LIMIT 1;"
    df: pl.DataFrame = conn.sql(sql).pl()
    return json.dumps(df.to_dicts())

def run_api() -> None:
  app: Any = APP
  uvicorn.run(app, host="0.0.0.0", port=8052, reload=True)
