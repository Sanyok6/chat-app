from django.contrib import admin

from . import models


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("creator", "name", "created_at")


admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.ChatRoom, ChatRoomAdmin)
