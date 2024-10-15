import json

from apps.chat.models import Message
from apps.user.models import User

from channels.generic.websocket import AsyncWebsocketConsumer 
from channels.db import database_sync_to_async
from channels.auth import login

class Consumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        self.user = self.scope['user']

        if self.user.is_authenticated:
            

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
        else:
            self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        if self.user.is_authenticated:

            text_data_json = json.loads(text_data)
            message_text = text_data_json["message"]

            message = await self.create_message(message_text, self.room_name)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message.message}
            )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
    
    @database_sync_to_async
    def create_message(self, message, room_name):
        # user = User.objects.create(phone_number='+996500800263')
        return Message.objects.create(message=message, room_name=room_name)