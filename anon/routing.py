from django.urls import path
from . import consumers

websocket_urlpatterns= [
    path('inbox/',consumers.ChatConsumer.as_asgi()),
]
