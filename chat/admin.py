from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'task_id', 'query', 'query_response', 'user', 
        'created_on', 'created_by', 'last_modified_on', 'last_modified_by'
    )
    search_fields = (
        'task_id', 'query', 'user__username', 
        'created_by__username', 'last_modified_by__username'
    )
    list_display_links = ('task_id', 'user')

admin.site.register(Message, MessageAdmin)
