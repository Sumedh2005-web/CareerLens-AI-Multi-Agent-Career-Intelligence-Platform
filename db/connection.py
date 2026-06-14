import os
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_config(key: str) -> str:
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

def get_engine():
    url = (
        f"postgresql+psycopg2://{get_config('DB_USER')}:{get_config('DB_PASSWORD')}"
        f"@{get_config('DB_HOST')}:{get_config('DB_PORT')}/{get_config('DB_NAME')}"
    )
    return create_engine(url)

def run_query(sql: str) -> list[dict]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


def get_engine():
    url = (
        f"postgresql+psycopg2://{get_config('DB_USER')}:{get_config('DB_PASSWORD')}"
        f"@{get_config('DB_HOST')}:{get_config('DB_PORT')}/{get_config('DB_NAME')}"
        f"?sslmode=require"
    )
    return create_engine(url)
