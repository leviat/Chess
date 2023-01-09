from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chess/room/(?P<room_name>[0-9]{1,9})$", consumers.ChessConsumer.as_asgi()
    ),
]
