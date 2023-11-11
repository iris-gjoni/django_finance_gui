from django.urls import path
from myapp.consumers import DashConsumer

websocket_urlpatterns = {
    path('ws/async_page/', DashConsumer.as_asgi()),
}
