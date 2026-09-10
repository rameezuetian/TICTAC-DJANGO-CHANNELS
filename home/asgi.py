"""
ASGI config for home project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from tictac.consumer import GameRoom

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')

django_asgi = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/game/(?P<room_code>[^/]+)/$', GameRoom.as_asgi()),
        ])
    ),
})