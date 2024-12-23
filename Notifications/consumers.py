# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            print("WebSocket connection attempt...")
            token = self.scope["query_string"].decode().split("=")[1]
            print(f"Token received: {token[:20]}...")  # Print first 20 chars of token
            user = await self.get_user_from_token(token)
            if user:
                print(f"User authenticated: {user.id}")
                self.user = user
                self.group_name = f"user_{user.id}"
                await self.channel_layer.group_add(self.group_name, self.channel_name)
                await self.accept()
                print("WebSocket connection accepted")
            else:
                print("User authentication failed")
                await self.close()
        except Exception as e:
            print(f"Connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            await self.channel_layer.group_send(
                self.group_name, {"type": "send_notification", "message": message}
            )
        except Exception as e:
            print(f"Receive error: {e}")

    async def send_notification(self, event):
        try:
            message = event["message"]
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "type": event.get("notification_type", "default"),
                        "user_name": event.get("user_name", ""),
                        "id": event.get("id", ""),
                        "profile_picture": event.get("profile_picture", ""),
                    }
                )
            )
        except Exception as e:
            print(f"Send notification error: {e}")

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user = get_user_model().objects.get(id=access_token["user_id"])
            return user
        except Exception:
            return None
