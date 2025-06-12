from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import APIKey

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None

        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
            key_obj.usage_count += 1
            key_obj.last_used = timezone.now()
            key_obj.save()
            return (key_obj.user, key_obj)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
