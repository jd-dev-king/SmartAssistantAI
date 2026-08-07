from __future__ import annotations

import os
from typing import Any

import requests

DEFAULT_URL = 'http://127.0.0.1:8010'
API_URL = os.getenv('EES_ASSISTANT_API_URL', DEFAULT_URL).rstrip('/')
TIMEOUT = float(os.getenv('EES_ASSISTANT_TIMEOUT', '1.5'))

EES_HINTS = (
    'ees ', 'ees universe', 'data moon', 'power grid', 'rc control', 'rc diagnostic',
    'pharma batch', 'parking', 'parked', 'visitor', 'manufacturing', 'asset health',
    'global supply', 'supply nexus', 'registered system'
)


def is_ees_question(message: str) -> bool:
    text = message.lower().strip()
    return any(hint in text for hint in EES_HINTS)


def health() -> dict[str, Any] | None:
    try:
        response = requests.get(f'{API_URL}/api/health', timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def ask(question: str) -> str | None:
    try:
        response = requests.post(
            f'{API_URL}/api/ees/query', json={'question': question}, timeout=max(TIMEOUT, 4.0)
        )
        response.raise_for_status()
        return response.json().get('answer')
    except requests.RequestException:
        return None


def sync_profile(profile: dict[str, Any]) -> bool:
    payload = {
        'name': profile.get('name'),
        'favoriteColor': profile.get('favorite_color') or profile.get('favoriteColor'),
        'job': profile.get('job'),
    }
    try:
        response = requests.post(f'{API_URL}/api/memory/profile', json=payload, timeout=TIMEOUT)
        return response.ok
    except requests.RequestException:
        return False


def fetch_profile() -> dict[str, Any] | None:
    try:
        response = requests.get(f'{API_URL}/api/memory/profile', timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get('profile') or {}
    except requests.RequestException:
        return None
