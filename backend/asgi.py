import os
from django.core.asgi import get_asgi_application

# Set the Django settings module path first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialize Django ASGI application early to avoid settings issues
django_asgi_app = get_asgi_application()

# Import the rest after Django is properly configured
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Notifications.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Use the pre-initialized django_asgi_app
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
