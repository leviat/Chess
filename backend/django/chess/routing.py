from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chess/(?P<room_name>[0-9]{1,9})/$", consumers.ChessConsumer.as_asgi()),
    re_path(r"ws/chess/(?P<room_name>9999999999)/$", consumers.ChessConsumer.as_asgi()),
]