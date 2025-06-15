import pytest
import httpx
import websockets
import asyncio
import json

BASE_HTTP = "http://localhost"
BASE_WS   = "ws://localhost/ws/chat/"

@pytest.mark.asyncio
async def test_healthz():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_HTTP}/healthz/")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"

@pytest.mark.asyncio
async def test_websocket_count():
    async with websockets.connect(BASE_WS) as ws:
        await ws.send("hello")
        msg = await asyncio.wait_for(ws.recv(), timeout=2)
        data = json.loads(msg)
        assert data.get("count") == 1