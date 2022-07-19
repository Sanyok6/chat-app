from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from . import consumers


router = DefaultRouter()
router.register('', views.MessageViewSet, basename='messaging')

urlpatterns = [] + router.urls

websocket_urlpatterns = [
    path("api/ws/", consumers.ChatConsumer.as_asgi()),
]
