from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<int:eId>/', consumers.ChatConsumer.as_asgi()),
]
