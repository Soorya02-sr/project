from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class UserOnlyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            # Check if the user is an admin; if so, deny access
            if user.is_staff or user.is_superuser:
                return None
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
