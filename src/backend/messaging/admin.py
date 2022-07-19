from django.contrib import admin

from . import models


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")


admin.site.register(models.Message, MessageAdmin)
