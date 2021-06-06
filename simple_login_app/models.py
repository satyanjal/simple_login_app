from _datetime import datetime
from enum import Enum
from mongoengine import *
from django.contrib.auth.hashers import make_password


class UserTypes(Enum):
    CLIENT = 0
    ADMIN = 1


class User(Document):
    firstname = StringField(default='')
    lastname = StringField(default='')
    username = StringField(default='')
    companyname = StringField(default='')
    password = StringField(default='')
    role = StringField(default='')
    email = StringField(default='')
    user_type = StringField(default=UserTypes.CLIENT)
    is_active = BooleanField(default=True)
    last_login = DateTimeField(default=datetime.now())
    date_created = DateTimeField(default=datetime.now())
    date_modified = DateTimeField(default=datetime.now())

    @staticmethod
    def create_user(data):
        user = User()
        user.username = data.get('username')
        user.password = make_password(data.get('password'))
        user.firstname = data.get('firstname')
        user.lastname = data.get('lastname')
        user.role = data.get('role')
        user.email = data.get('email')
        user.user_type = data.get('user_type')
        user.companyname = data.get('companyname')
        user.save()
        return user

    @classmethod
    def get_user_by_username(cls, username):
        try:
            return cls.objects.get(username=username)
        except:
            return None

    @classmethod
    def get_all_admin_user(cls):
        return cls.objects.filter(user_type=UserTypes.ADMIN)


class Client(Document):
    client = ReferenceField(User)
    last_login = DateTimeField(default=datetime.now())
    is_authorized = BooleanField(default=False)

    @classmethod
    def get_all_client(cls):
        try:
            return cls.objects.all()
        except:
            return None

    @classmethod
    def get_client(cls, username):
        try:
            user = User.get_user_by_username(username)
            return cls.objects.get(client=user)
        except:
            return None

    @classmethod
    def authorize_client(cls, username, is_authorized):
        user = User.get_user_by_username(username)
        client = cls.objects.get(client=user)
        client.is_authorized = is_authorized
        client.save()
        return client

    @classmethod
    def update_client_login(cls, username):
        user = User.get_user_by_username(username)
        client = cls.objects.filter(client=user)
        if client:
            client.last_login = datetime.now()
            client.is_authorized = False
        else:
            client = Client()
            client.client = user
        client.save()
        return client



