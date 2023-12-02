from django.contrib.auth.backends import ModelBackend
from .models import Registerinfo

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Registerinfo.objects.get(email=email)
        except Registerinfo.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None


