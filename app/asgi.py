import os
import asyncio
import datetime
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from app.chat import routing as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

HEARTBEAT_SECS= 10
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(chat_routing.websocket_urlpatterns)
})

# heartbeat
async def _heartbeat_loop():
    channel_layer = get_channel_layer()
    while True:
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        await channel_layer.group_send(
            "heartbeat",
            {"type": "heartbeat", "ts": ts}
        )
        await asyncio.sleep(HEARTBEAT_SECS)

async def _startup():
    await asyncio.sleep(1)
    asyncio.create_task(_heartbeat_loop())

asyncio.get_event_loop().create_task(_startup())