# Smart Assistant AI v3.0.0 — EES Integration Setup

Smart Assistant AI remains a standalone desktop + browser assistant. The EES backend is optional.
If the EES service is stopped, calculator, weather, Wikipedia, dictionary, jokes, voice, local browser memory,
file analysis, charts, system monitoring, file search, app launcher, and Local AI continue to work.

## Architecture

```text
Smart Assistant AI
├── Standalone tools (always available)
├── Local memory (JSON / localStorage)
├── Local AI (optional WebLLM)
└── EES Connected mode (optional)
    ├── assistant.* persistent memory
    ├── parking_access.* read-only queries
    ├── ees_registry.* read-only queries
    ├── rc_controls.* read-only queries
    ├── pharma.* read-only queries
    ├── power_grid.* read-only context
    ├── supply.* read-only context
    └── analytics.* read-only context
```

The EES API only writes to `assistant.*` plus its own `ees_registry` registration. Operational domains remain read-only.

## 1. Create Python 3.12 environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 2. Configure backend

```bash
cp backend/.env.example backend/.env
```

Set your canonical database URL, for example:

```env
DATABASE_URL=postgresql://YOUR_POSTGRES_USER@localhost:5432/ees_data_platform
ASSISTANT_OWNER_KEY=default
CORS_ORIGINS=http://localhost:5502,http://127.0.0.1:5502
```

## 3. Initialize assistant schema

```bash
cd backend
python init_db.py
```

Expected:

```text
Initialized ees_data_platform.assistant and registered Smart Assistant AI with EES Data Moon.
```

## 4. Start Smart Assistant EES API

From `backend/`:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8010
```

Health check:

```bash
curl http://127.0.0.1:8010/api/health
```

## 5. Start the browser edition

From the project root:

```bash
python3 -m http.server 5502
```

Open:

```text
http://localhost:5502/docs/
```

In **Settings → Assistant mode**, select **EES Connected**.

## 6. Desktop edition

The desktop assistant automatically detects EES-related questions when the EES API is running.
It does not require EES to start.

```bash
python main.py
```

Optional desktop API override:

```bash
export EES_ASSISTANT_API_URL=http://127.0.0.1:8010
```

## Smoke-test prompts

Standalone:

```text
calculate 125 * 8
what is the weather in Philadelphia, PA?
define automation
wiki Nikola Tesla
my name is Jeremiah
what is my name
```

EES Connected:

```text
How many employees are parked right now?
Which visitors are currently parked?
What systems are registered in Data Moon?
What is the latest RC diagnostic?
What is the latest Pharma batch?
What Power Grid information is available?
What Manufacturing Intelligence data is connected?
```

## Persistent memory

Local memory remains the fallback. When the EES API is reachable, profile memory can synchronize to:

```text
assistant.memories
assistant.conversations
assistant.messages
assistant.preferences
assistant.system_context
assistant.action_log
```

This means the assistant remains useful by itself while gaining persistent cross-session EES memory when connected.
