from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views
from . import consumers


router = DefaultRouter()
router.register('', views.ChatRoomsViewSet, basename='chat_rooms')

messages_router = NestedDefaultRouter(router, '', lookup='room')
messages_router.register('messages', views.MessageViewSet, basename='messages_viewset')

urlpatterns = router.urls + messages_router.urls

websocket_urlpatterns = [
    re_path(r'api/ws/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
