from pytest import mark
from telethon import TelegramClient
from telethon.tl.custom.message import Message


@mark.asyncio
async def test_bot_works(client: TelegramClient):
    async with client.conversation("@VeryVerySmart_bot", timeout=15) as conv:
        user_message = "some text"
        await conv.send_message("some text")
        resp: Message = await conv.get_response()
        assert resp.raw_text.startswith(user_message)
