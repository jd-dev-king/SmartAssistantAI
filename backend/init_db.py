from __future__ import annotations

import uuid
from pathlib import Path

from db import connection

BASE = Path(__file__).resolve().parent

DATASETS = [
    ('assistant-memories', 'Assistant Memories', 'assistant', 'memories', 'table'),
    ('assistant-conversations', 'Assistant Conversations', 'assistant', 'conversations', 'table'),
    ('assistant-messages', 'Assistant Messages', 'assistant', 'messages', 'table'),
    ('assistant-preferences', 'Assistant Preferences', 'assistant', 'preferences', 'table'),
    ('assistant-system-context', 'Assistant System Context', 'assistant', 'system_context', 'table'),
    ('assistant-action-log', 'Assistant Action Log', 'assistant', 'action_log', 'table'),
]


def main():
    sql = (BASE / 'sql' / '001_assistant_schema.sql').read_text(encoding='utf-8')
    with connection() as con:
        with con.cursor() as cur:
            cur.execute(sql)

            # Register with the EES Universal Data Moon when its registry exists.
            cur.execute("SELECT to_regclass('ees_registry.systems') AS rel")
            if cur.fetchone()['rel']:
                system_key = 'smart-assistant-ai'
                cur.execute(
                    'SELECT system_id FROM ees_registry.systems WHERE system_key = %s',
                    (system_key,),
                )
                row = cur.fetchone()
                if row:
                    system_id = row['system_id']
                    cur.execute(
                        '''
                        UPDATE ees_registry.systems
                        SET system_name=%s, domain=%s, system_type=%s, status='active',
                            data_role=%s, primary_database='ees_data_platform', updated_at=NOW()
                        WHERE system_id=%s
                        ''',
                        (
                            'Smart Assistant AI', 'artificial-intelligence',
                            'assistant-intelligence-layer', 'cross-domain-intelligence', system_id,
                        ),
                    )
                else:
                    system_id = uuid.uuid4()
                    cur.execute(
                        '''
                        INSERT INTO ees_registry.systems
                        (system_id, system_name, system_key, domain, system_type, description,
                         status, data_role, primary_database, owner_name)
                        VALUES (%s,%s,%s,%s,%s,%s,'active',%s,'ees_data_platform',%s)
                        ''',
                        (
                            system_id, 'Smart Assistant AI', system_key,
                            'artificial-intelligence', 'assistant-intelligence-layer',
                            'Standalone Smart Assistant AI with optional EES Universe database intelligence and persistent memory.',
                            'cross-domain-intelligence', 'EES Universe',
                        ),
                    )

                cur.execute("SELECT to_regclass('ees_registry.datasets') AS rel")
                if cur.fetchone()['rel']:
                    for dataset_key, dataset_name, schema_name, object_name, object_type in DATASETS:
                        cur.execute(
                            '''
                            INSERT INTO ees_registry.datasets
                            (dataset_id, system_id, dataset_name, dataset_key, domain, database_name,
                             schema_name, object_name, object_type, source_type, classification,
                             refresh_mode, description, is_active)
                            VALUES (%s,%s,%s,%s,%s,'ees_data_platform',%s,%s,%s,'postgresql',
                                    'operational','realtime',%s,TRUE)
                            ON CONFLICT (system_id, dataset_key)
                            DO UPDATE SET dataset_name=EXCLUDED.dataset_name,
                                          schema_name=EXCLUDED.schema_name,
                                          object_name=EXCLUDED.object_name,
                                          object_type=EXCLUDED.object_type,
                                          is_active=TRUE,
                                          updated_at=NOW()
                            ''',
                            (
                                uuid.uuid4(), system_id, dataset_name, dataset_key,
                                'artificial-intelligence', schema_name, object_name, object_type,
                                f'Smart Assistant AI {dataset_name.lower()} dataset.',
                            ),
                        )
        con.commit()

    print('Initialized ees_data_platform.assistant and registered Smart Assistant AI with EES Data Moon.')


if __name__ == '__main__':
    main()
