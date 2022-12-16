import json
import random
from datetime import datetime

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection
from chess.models import ChessMatch, User
from chess.serializers import ChessMatchSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import async_to_sync

# connect
# setup or load room
# register or load user


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        try:  # load match
            chess_match = ChessMatch.objects.get(id=self.room_name)
            chess_match.last_accessed = datetime.now()
            chess_match.save()

        except (ObjectDoesNotExist):  # register match
            data = {'id': self.room_name}
            chess_match = ChessMatchSerializer(data=data)
            if chess_match.is_valid():
                chess_match.save()
                chess_match = ChessMatch.objects.get(id=self.room_name)
            else:
                err_msg = f"Errors: {chess_match.errors}."
                print(err_msg)
                raise DenyConnection(err_msg)

        print(self.scope["session"].session_key)
        if self.scope["session"].session_key is None:
            err_msg = "No cookies set. User cannot be identified with a session."
            print(err_msg)
            raise DenyConnection(err_msg)

        try:  # load user
            user = chess_match.users.get(
                chess_match=self.room_name,
                session_key=self.scope["session"].session_key,
            )
            self.user_name = user.name
        except User.DoesNotExist:  # register user
            self.user_name = "user" + str(chess_match.users.count())
            data = {
                "chess_match": self.room_name,
                "session_key": self.scope["session"].session_key,
                "name": self.user_name,
            }

            user = UserSerializer(data=data)
            if user.is_valid():
                user.save()
            else:
                err_msg = (
                    "User could not be loaded or created. Please report this as a bug."
                )
                print(err_msg)
                raise DenyConnection(err_msg)

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json["text"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {"type": "chat_message", "user": self.user_name, "text": message_text},
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({"user": event["user"], "text": event["text"]}))
