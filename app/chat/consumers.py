import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger('chat')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info('ws_connect')
        await self.accept()

    async def receive(self, text_data):
        logger.info('ws_message', extra={'payload': text_data})
        await self.send(text_data=text_data)

    async def disconnect(self, close_code):
        logger.info('ws_disconnect', extra={'code': close_code})