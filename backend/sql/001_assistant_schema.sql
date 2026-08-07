CREATE SCHEMA IF NOT EXISTS assistant;

CREATE TABLE IF NOT EXISTS assistant.memories (
    memory_id BIGSERIAL PRIMARY KEY,
    owner_key VARCHAR(120) NOT NULL DEFAULT 'default',
    memory_key VARCHAR(120) NOT NULL,
    memory_value TEXT NOT NULL,
    category VARCHAR(80) NOT NULL DEFAULT 'profile',
    source VARCHAR(80) NOT NULL DEFAULT 'smart-assistant-ai',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (owner_key, memory_key)
);

CREATE TABLE IF NOT EXISTS assistant.conversations (
    session_id VARCHAR(160) PRIMARY KEY,
    owner_key VARCHAR(120) NOT NULL DEFAULT 'default',
    title VARCHAR(250) NOT NULL DEFAULT 'New conversation',
    source VARCHAR(80) NOT NULL DEFAULT 'smart-assistant-ai',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assistant.messages (
    message_id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(160) NOT NULL REFERENCES assistant.conversations(session_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    channel VARCHAR(40) NOT NULL DEFAULT 'chat',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_assistant_messages_session
    ON assistant.messages(session_id, created_at);

CREATE TABLE IF NOT EXISTS assistant.preferences (
    preference_id BIGSERIAL PRIMARY KEY,
    owner_key VARCHAR(120) NOT NULL DEFAULT 'default',
    preference_key VARCHAR(120) NOT NULL,
    preference_value TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (owner_key, preference_key)
);

CREATE TABLE IF NOT EXISTS assistant.system_context (
    context_id BIGSERIAL PRIMARY KEY,
    context_key VARCHAR(160) NOT NULL UNIQUE,
    context_value JSONB NOT NULL DEFAULT '{}'::jsonb,
    source_system VARCHAR(160),
    refreshed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assistant.action_log (
    action_id BIGSERIAL PRIMARY KEY,
    owner_key VARCHAR(120) NOT NULL DEFAULT 'default',
    action_type VARCHAR(120) NOT NULL,
    target_system VARCHAR(160),
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
