from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from simple_login_app.models import User


class UserAuth(BaseBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user and check_password(password, user.password):
                return user
        except:
            return None




