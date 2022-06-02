import pytest
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ["TG_TEST_ID"])
api_hash = os.environ["TG_TEST_HASH"]
session_str = os.environ["TELEGRAM_TEST_SESSION"]

@pytest.fixture
async def client():
    client = TelegramClient(
        StringSession(session_str), api_id, api_hash,
        sequential_updates=True
    )
    client.start()
    await client.connect()
    await client.get_me()

    yield client

    await client.disconnect()
    await client.disconnected