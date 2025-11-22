import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Profile


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return

        self.group_name = "online_users"

        # join presence group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

        # broadcast that this user is online
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence_event",
                "event": "online",
                "user_id": user.id,
                "username": user.username,
                "avatar_url": await self.get_avatar_url(user),
            },
        )

    async def disconnect(self, close_code):
        user = self.scope["user"]

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

        if not user.is_anonymous:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "presence_event",
                    "event": "offline",
                    "user_id": user.id,
                    "username": user.username,
                },
            )

    async def presence_event(self, event):
        # send to client
        await self.send(
            text_data=json.dumps(
                {
                    "type": "presence",
                    "event": event["event"],  # online/offline
                    "user_id": event["user_id"],
                    "username": event["username"],
                    "avatar_url": event.get("avatar_url", ""),
                }
            )
        )

    @sync_to_async
    def get_avatar_url(self, user: User) -> str:
        profile, _ = Profile.objects.get_or_create(user=user)
        if profile.avatar and hasattr(profile.avatar, "url"):
            return profile.avatar.url
        return ""
