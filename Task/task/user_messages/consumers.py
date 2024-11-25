import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user_id = self.scope['url_route']['kwargs']['user_id']
            self.group_name = f"user_{self.user_id}"

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            print(f"WebSocket подключён: user_id={self.user_id}")
        except KeyError as e:
            print(f"Ошибка: {e}")
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        owner = text_data_json["owner"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name, {"type": "send_notification", "owner": owner, "sender_channel": self.group_name}
        )

    async def send_notification(self, event):
        owner = event["owner"]
        type_msg = event['type']
        title = event['title']
        text = event['text']
        payload = {
            'owner': owner,
            'title': title,
            'text': text
        }
        await self.send(text_data=json.dumps(owner))