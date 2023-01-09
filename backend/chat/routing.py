from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[0-9]{1,9})/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>9999999999)/$", consumers.ChatConsumer.as_asgi()),
]