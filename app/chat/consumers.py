import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger('chat')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info('ws_connect')
        await self.accept()
    
    async def connect(self):
        self.counter = 0
        await self.channel_layer.group_add("heartbeat", self.channel_name)
        logger.info("ws_connect", extra={"connection": self.channel_name})
        await self.accept()

    async def receive(self, text_data):
        self.counter += 1
        logger.info("ws_message_received", extra={"count": self.counter})
        await self.send(text_data=json.dumps({"count": self.counter}))

    async def disconnect(self, close_code):
        await self.send(text_data=json.dumps({
            "bye": True,
            "total": self.counter
        }))
        await self.channel_layer.group_discard("heartbeat", self.channel_name)
        logger.info("ws_disconnect", extra={"code": close_code})

    async def heartbeat(self, event):
        await self.send(text_data=json.dumps({
            "ts": event["ts"]
        }))