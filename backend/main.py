from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from psycopg import sql

from db import connection, relation_exists

load_dotenv()

OWNER_KEY = os.getenv('ASSISTANT_OWNER_KEY', 'default')
CORS_ORIGINS = [x.strip() for x in os.getenv(
    'CORS_ORIGINS',
    'http://localhost:5502,http://127.0.0.1:5502'
).split(',') if x.strip()]

app = FastAPI(
    title='Smart Assistant AI — EES Intelligence API',
    version='3.0.0',
    description='Optional EES Universe intelligence and persistent-memory layer. Standalone assistant tools remain independent.',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class MemoryWrite(BaseModel):
    value: str
    category: str = 'profile'


class ProfileSync(BaseModel):
    name: str | None = None
    favoriteColor: str | None = None
    job: str | None = None


class MessageWrite(BaseModel):
    role: str = Field(pattern='^(user|assistant|system)$')
    content: str
    title: str = 'New conversation'
    channel: str = 'chat'


class EesQuestion(BaseModel):
    question: str


def _memory_map(con) -> dict[str, str]:
    with con.cursor() as cur:
        cur.execute(
            '''SELECT memory_key, memory_value FROM assistant.memories
               WHERE owner_key=%s ORDER BY memory_key''',
            (OWNER_KEY,),
        )
        return {r['memory_key']: r['memory_value'] for r in cur.fetchall()}


def _upsert_memory(con, key: str, value: str, category='profile') -> None:
    with con.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO assistant.memories(owner_key,memory_key,memory_value,category)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT(owner_key,memory_key)
            DO UPDATE SET memory_value=EXCLUDED.memory_value,
                          category=EXCLUDED.category,
                          updated_at=NOW()
            ''',
            (OWNER_KEY, key, value, category),
        )


def _schema_relations(con, schema_name: str) -> list[str]:
    with con.cursor() as cur:
        cur.execute(
            '''SELECT table_name FROM information_schema.tables WHERE table_schema=%s
               UNION SELECT table_name FROM information_schema.views WHERE table_schema=%s
               ORDER BY table_name''',
            (schema_name, schema_name),
        )
        return [r['table_name'] for r in cur.fetchall()]


def _format_rows(rows: list[dict[str, Any]], max_rows=8) -> str:
    if not rows:
        return 'No matching records were found.'
    pieces = []
    for row in rows[:max_rows]:
        clean = []
        for k, v in row.items():
            if v is None:
                continue
            if isinstance(v, (dict, list)):
                v = json.dumps(v, default=str)
            clean.append(f'{k}: {v}')
        pieces.append(' • ' + ', '.join(clean))
    return '\n'.join(pieces)


def _latest_json_row(con, schema_name: str, table_name: str, order_candidates: list[str]) -> dict | None:
    with con.cursor() as cur:
        cur.execute(
            '''SELECT column_name FROM information_schema.columns
               WHERE table_schema=%s AND table_name=%s''',
            (schema_name, table_name),
        )
        cols = {r['column_name'] for r in cur.fetchall()}
        order = next((c for c in order_candidates if c in cols), None)
        query = sql.SQL('SELECT to_jsonb(t) AS row FROM {}.{} t').format(
            sql.Identifier(schema_name), sql.Identifier(table_name)
        )
        if order:
            query += sql.SQL(' ORDER BY {} DESC NULLS LAST').format(sql.Identifier(order))
        query += sql.SQL(' LIMIT 1')
        cur.execute(query)
        result = cur.fetchone()
        return result['row'] if result else None


def answer_ees(con, question: str) -> tuple[str, str, list[dict[str, Any]]]:
    q = re.sub(r'\s+', ' ', question.lower()).strip()

    # Parking — active occupancy and rosters.
    if ('park' in q or 'parking' in q) and relation_exists(con, 'parking_access', 'parking_sessions'):
        if 'visitor' in q and any(x in q for x in ('who', 'which', 'list', 'inside', 'currently')):
            with con.cursor() as cur:
                cur.execute('''
                    SELECT COALESCE(vp.visitor_code, ps.vehicle_identifier) AS visitor,
                           ps.vehicle_identifier, sp.space_number, ps.entry_time
                    FROM parking_access.parking_sessions ps
                    JOIN parking_access.parking_spaces sp ON sp.space_id=ps.space_id
                    LEFT JOIN parking_access.visitor_passes vp ON vp.visitor_pass_id=ps.visitor_pass_id
                    WHERE ps.session_status='ACTIVE' AND ps.occupant_type='VISITOR'
                    ORDER BY ps.entry_time DESC
                ''')
                rows = cur.fetchall()
            return (f'There are {len(rows)} visitors currently parked.' + ('\n' + _format_rows(rows) if rows else ''), 'parking_access', rows)

        if 'employee' in q and any(x in q for x in ('who', 'which', 'list', 'inside', 'currently')):
            with con.cursor() as cur:
                cur.execute('''
                    SELECT e.employee_number, e.display_name, ps.vehicle_identifier,
                           sp.space_number, ps.entry_time
                    FROM parking_access.parking_sessions ps
                    JOIN parking_access.parking_spaces sp ON sp.space_id=ps.space_id
                    LEFT JOIN parking_access.employee_vehicles ev ON ev.vehicle_identifier=ps.vehicle_identifier
                    LEFT JOIN parking_access.employees e ON e.employee_id=ev.employee_id
                    WHERE ps.session_status='ACTIVE' AND ps.occupant_type='EMPLOYEE'
                    ORDER BY ps.entry_time DESC
                ''')
                rows = cur.fetchall()
            return (f'There are {len(rows)} employees currently parked.' + ('\n' + _format_rows(rows) if rows else ''), 'parking_access', rows)

        with con.cursor() as cur:
            cur.execute('''
                SELECT COUNT(*) FILTER (WHERE session_status='ACTIVE') AS occupied,
                       COUNT(*) FILTER (WHERE session_status='ACTIVE' AND occupant_type='EMPLOYEE') AS employees,
                       COUNT(*) FILTER (WHERE session_status='ACTIVE' AND occupant_type='VISITOR') AS visitors
                FROM parking_access.parking_sessions
            ''')
            row = cur.fetchone()
            cur.execute("SELECT COUNT(*) AS total FROM parking_access.parking_spaces")
            total = cur.fetchone()['total']
        occupied = row['occupied'] or 0
        return (f'Pharma parking is {occupied}/{total} occupied: {row["employees"] or 0} employees and {row["visitors"] or 0} visitors. {max(total-occupied,0)} spaces remain.', 'parking_access', [row])

    # EES registry / Data Moon.
    if any(x in q for x in ('registered system', 'data moon', 'ees system', 'systems are connected', 'systems connected')) and relation_exists(con, 'ees_registry', 'systems'):
        with con.cursor() as cur:
            cur.execute('''SELECT system_name, domain, system_type, status
                           FROM ees_registry.systems ORDER BY system_name''')
            rows = cur.fetchall()
        return (f'EES Data Moon currently registers {len(rows)} systems:\n' + _format_rows(rows, 20), 'ees_registry', rows)

    # RC Controls latest diagnostic/event.
    if any(x in q for x in ('rc control', 'rc diagnostic', 'latest diagnostic')) and relation_exists(con, 'rc_controls', 'control_events'):
        with con.cursor() as cur:
            cur.execute('''SELECT event_type, severity, event_message, occurred_at, metadata
                           FROM rc_controls.control_events
                           ORDER BY occurred_at DESC LIMIT 1''')
            row = cur.fetchone()
        if row:
            return ('Latest RC Controls event:\n' + _format_rows([row]), 'rc_controls', [row])
        return ('RC Controls is connected, but no control events are currently recorded.', 'rc_controls', [])

    # Pharma latest batch — use schema-aware lookup so this survives modest schema evolution.
    if ('pharma' in q or 'batch' in q) and relation_exists(con, 'pharma', 'batches'):
        row = _latest_json_row(con, 'pharma', 'batches', ['started_at', 'created_at', 'updated_at', 'batch_id'])
        if row:
            return ('Latest available Pharma batch record:\n' + _format_rows([row]), 'pharma', [row])
        return ('The Pharma schema is connected, but no batch rows are available.', 'pharma', [])

    # Power Grid — provide current catalog plus latest likely alert if available.
    if any(x in q for x in ('power grid', 'power alert', 'grid alert', 'power')):
        relations = _schema_relations(con, 'power_grid')
        for candidate in ('alerts', 'power_alerts', 'asset_alerts'):
            if candidate in relations:
                row = _latest_json_row(con, 'power_grid', candidate, ['occurred_at', 'created_at', 'timestamp', 'alert_id'])
                if row:
                    return (f'Latest Power Grid alert from power_grid.{candidate}:\n' + _format_rows([row]), 'power_grid', [row])
        return (f'Power Grid is connected. Available power_grid relations: {", ".join(relations) if relations else "none currently populated"}.', 'power_grid', [])

    # Supply / Manufacturing / analytics catalog.
    for keyword, schema_name, label in (
        ('supply', 'supply', 'Global Supply'),
        ('manufacturing', 'analytics', 'Manufacturing Intelligence'),
        ('asset health', 'analytics', 'Asset Health Analytics'),
    ):
        if keyword in q:
            relations = _schema_relations(con, schema_name)
            return (f'{label} is connected through the {schema_name} schema. Available relations: {", ".join(relations) if relations else "none currently populated"}.', schema_name, [])

    # General cross-domain status.
    with con.cursor() as cur:
        cur.execute('''SELECT schema_name FROM information_schema.schemata
                       WHERE schema_name IN ('ees_registry','power_grid','rc_controls','pharma','supply','analytics','parking_access','assistant')
                       ORDER BY schema_name''')
        schemas = [r['schema_name'] for r in cur.fetchall()]
    return (
        'EES Connected mode is online. I can query parking occupancy/rosters, Data Moon systems, '
        'RC Controls events, Pharma batch context, Power Grid context, Supply, and Manufacturing Intelligence. '
        f'Connected schemas currently visible: {", ".join(schemas)}.',
        'ees_data_platform',
        [],
    )


@app.get('/api/health')
def health():
    with connection() as con:
        with con.cursor() as cur:
            cur.execute('SELECT current_database() AS database, current_user AS db_user, NOW() AS server_time')
            row = cur.fetchone()
    return {'ok': True, 'service': 'smart-assistant-ai', 'version': '3.0.0', **row}


@app.get('/api/ees/context')
def ees_context():
    with connection() as con:
        with con.cursor() as cur:
            cur.execute('''SELECT schema_name FROM information_schema.schemata
                           WHERE schema_name IN ('ees_registry','power_grid','rc_controls','pharma','supply','analytics','parking_access','assistant')
                           ORDER BY schema_name''')
            schemas = [r['schema_name'] for r in cur.fetchall()]
        systems = []
        if relation_exists(con, 'ees_registry', 'systems'):
            with con.cursor() as cur:
                cur.execute('SELECT system_name, domain, status FROM ees_registry.systems ORDER BY system_name')
                systems = cur.fetchall()
    return {'ok': True, 'schemas': schemas, 'systems': systems}


@app.post('/api/ees/query')
def ees_query(body: EesQuestion):
    if not body.question.strip():
        raise HTTPException(400, 'question is required')
    with connection() as con:
        answer, domain, data = answer_ees(con, body.question)
        with con.cursor() as cur:
            cur.execute(
                '''INSERT INTO assistant.action_log(owner_key, action_type, target_system, details)
                   VALUES (%s,'ees-query',%s,%s::jsonb)''',
                (OWNER_KEY, domain, json.dumps({'question': body.question, 'answer': answer})),
            )
        con.commit()
    return {'ok': True, 'answer': answer, 'domain': domain, 'data': data}


@app.get('/api/memory/profile')
def get_profile():
    with connection() as con:
        memories = _memory_map(con)
    return {
        'ok': True,
        'profile': {
            'name': memories.get('name'),
            'favoriteColor': memories.get('favoriteColor') or memories.get('favorite_color'),
            'job': memories.get('job'),
        },
        'memories': memories,
    }


@app.post('/api/memory/profile')
def sync_profile(body: ProfileSync):
    with connection() as con:
        for key, value in body.model_dump().items():
            if value is not None and str(value).strip():
                _upsert_memory(con, key, str(value).strip(), 'profile')
        con.commit()
        profile = _memory_map(con)
    return {'ok': True, 'memories': profile}


@app.put('/api/memory/{memory_key}')
def put_memory(memory_key: str, body: MemoryWrite):
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,120}', memory_key):
        raise HTTPException(400, 'invalid memory key')
    with connection() as con:
        _upsert_memory(con, memory_key, body.value, body.category)
        con.commit()
    return {'ok': True, 'memory_key': memory_key, 'value': body.value}


@app.delete('/api/memory')
def clear_memories():
    with connection() as con:
        with con.cursor() as cur:
            cur.execute('DELETE FROM assistant.memories WHERE owner_key=%s', (OWNER_KEY,))
        con.commit()
    return {'ok': True}


@app.post('/api/conversations/{session_id}/messages')
def save_conversation_message(session_id: str, body: MessageWrite):
    if len(session_id) > 160:
        raise HTTPException(400, 'session_id is too long')
    with connection() as con:
        with con.cursor() as cur:
            cur.execute(
                '''INSERT INTO assistant.conversations(session_id,owner_key,title)
                   VALUES (%s,%s,%s)
                   ON CONFLICT(session_id) DO UPDATE SET title=EXCLUDED.title, updated_at=NOW()''',
                (session_id, OWNER_KEY, body.title[:250]),
            )
            cur.execute(
                '''INSERT INTO assistant.messages(session_id,role,content,channel)
                   VALUES (%s,%s,%s,%s)''',
                (session_id, body.role, body.content, body.channel),
            )
        con.commit()
    return {'ok': True}


@app.get('/api/conversations/{session_id}/messages')
def get_conversation_messages(session_id: str):
    with connection() as con:
        with con.cursor() as cur:
            cur.execute(
                '''SELECT role, content, channel, created_at
                   FROM assistant.messages WHERE session_id=%s ORDER BY created_at, message_id''',
                (session_id,),
            )
            rows = cur.fetchall()
    return {'ok': True, 'messages': rows}
