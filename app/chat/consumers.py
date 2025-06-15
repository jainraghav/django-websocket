import json
import logging
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from app.metrics import total_messages, active_connections, error_count, last_shutdown

logger = logging.getLogger('chat')

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.counter = 0
        active_connections.inc()
        await self.channel_layer.group_add("heartbeat", self.channel_name)
        logger.info("ws_connect", extra={"connection": self.channel_name})
        await self.accept()

    async def receive(self, text_data):
        try:
            self.counter += 1
            total_messages.inc()
            logger.info("ws_message_received", extra={"count": self.counter})
            await self.send(text_data=json.dumps({"count": self.counter}))
        except Exception as e:
            error_count.inc()
            logger.exception("error in receive")

    async def disconnect(self, close_code):

        last_shutdown.set(time.time())
        active_connections.dec()

        try:
            await self.send(text_data=json.dumps({
                "bye": True, "total": self.counter
            }))
        except RuntimeError:
            pass

        await self.channel_layer.group_discard("heartbeat", self.channel_name)
        logger.info("ws_disconnect", extra={"code": close_code})

    async def heartbeat(self, event):
        await self.send(text_data=json.dumps({
            "ts": event["ts"]
        }))