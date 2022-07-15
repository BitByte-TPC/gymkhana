import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.db import models


class Token(models.Model):
    token = models.CharField(max_length=30)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def find_or_create(user):
        token = Token.objects.filter(user=user).first()
        if not token:
            return Token.objects.create(token=uuid.uuid4().hex, user=user)
        return token

    @staticmethod
    def if_expired_get_new(token, user):
        token_life = (datetime.now(timezone.utc) - token.created_at).days
        if(token_life >= settings.AUTH_ALLOWED_TOKEN_LIFE_IN_DAYS):
            token.delete()
            return Token.objects.create(token=uuid.uuid4().hex, user=user)
        return token
