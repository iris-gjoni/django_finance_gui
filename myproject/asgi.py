"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

normal_asgi_application = get_asgi_application()


# application = ProtocolTypeRouter({
#     "http": normal_asgi_application,
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
#     )
# })

application = ProtocolTypeRouter({
    "http": normal_asgi_application,
    'websocket': URLRouter(
        routing.websocket_urlpatterns
    ),
})
