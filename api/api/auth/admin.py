from django.contrib import admin

from api.auth.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass
