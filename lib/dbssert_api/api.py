from fastapi import FastAPI
from typing import Any
from os import environ as env
import uvicorn
import duckdb
import polars as pl

APP: Any = FastAPI()
DBSSERT_PATH: str = env["DBSSERT_PATH"]

@APP.get("/curies-with-ner")
def get_curies_with_ner(entity: str) -> list[dict[str, Any]]:
  p: str = DBSSERT_PATH
  with duckdb.connect(p, read_only=True) as conn:
    entity = entity.lower()
    sql: str = f"""
    SELECT 
      C.CURIE,
      C.PREFERRED_NAME,
      S.SYNONYM,
      G.CATEGORY_NAME,
      C.TAXON_ID
    FROM SYNONYMS S
    JOIN CURIES C ON S.CURIE_ID = C.CURIE_ID 
    JOIN CATEGORIES G ON C.CATEGORY_ID = G.CATEGORY_ID
    WHERE S.SYNONYM = '{entity}' LIMIT 20;
    """
    df: pl.DataFrame = conn.sql(sql).pl()
    return df.to_dicts()

@APP.get("/cannoical-curie-information")
def get_cannoical_curie_information(curie: str) -> list[dict[str, Any]]:
  p: str = DBSSERT_PATH
  with duckdb.connect(p, read_only=True) as conn:
    sql: str = f"""
    SELECT
      C.CURIE,
      C.PREFERRED_NAME,
      G.CATEGORY_NAME,
      C.TAXON_ID
    FROM CURIES C 
    JOIN CATEGORIES G ON C.CATEGORY_ID = G.CATEGORY_ID
    WHERE C.CURIE = '{curie}' LIMIT 10;
    """
    df: pl.DataFrame = conn.sql(sql).pl()
    return df.to_dicts()

@APP.get("/health")
def health() -> str:
  return "ok"

def serve_api() -> None:
  app: Any = APP
  uvicorn.run(app, host="0.0.0.0", port=8052)
