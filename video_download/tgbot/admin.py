from django.contrib import admin

from tgbot.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'user_name', 'first_name', 'last_name', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", ]
    search_fields = ('user_name', 'user_id')

