from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv(Path(__file__).with_name('.env'))

DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
if not DATABASE_URL:
    raise RuntimeError(
        'DATABASE_URL is not set. Copy backend/.env.example to backend/.env '
        'and point it to ees_data_platform.'
    )


@contextmanager
def connection():
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as con:
        yield con


def relation_exists(con, schema: str, relation: str) -> bool:
    with con.cursor() as cur:
        cur.execute(
            '''
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = %s AND table_name = %s
                UNION ALL
                SELECT 1
                FROM information_schema.views
                WHERE table_schema = %s AND table_name = %s
            ) AS exists
            ''',
            (schema, relation, schema, relation),
        )
        return bool(cur.fetchone()['exists'])
