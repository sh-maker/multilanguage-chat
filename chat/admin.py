# admin.py
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'translated_content', 'timestamp')
    search_fields = ('sender', 'content', 'translated_content')



# message@gmail.com
# 123456