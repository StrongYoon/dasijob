# jobs/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = f"user_{self.user.id}_notifications"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "message": event["message"],
            "data": event["data"]
        }))


class JobUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = f"user_{self.user.id}_updates"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def job_update(self, event):
        """Send job update to WebSocket"""
        await self.send(text_data=json.dumps({
            "type": "job_update",
            "data": event["data"]
        }))

    async def application_update(self, event):
        """Send application status update to WebSocket"""
        await self.send(text_data=json.dumps({
            "type": "application_update",
            "data": event["data"]
        }))