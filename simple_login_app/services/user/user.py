import datetime

from simple_login_app.models import User, Client
from simple_login_app.utils import trigger_client_login_request_mail


class UserService:

    @staticmethod
    def create_user(data):
        return User.create_user(data)

    @staticmethod
    def get_user(username):
        return User.get_user_by_username(username)


class ClientService:

    @staticmethod
    def authorize_client(username, is_authorized):
        return Client.authorize_client(username, is_authorized)

    @staticmethod
    def get_client(username):
        return Client.get_client(username)

    @staticmethod
    def update_client_login(username):
        return Client.update_client_login(username)

    @staticmethod
    def client_login_request():
        all_clients = Client.get_all_client()
        for client in all_clients:
            if client.last_login > datetime.datetime.now() - datetime.timedelta(minutes=30):
                trigger_client_login_request_mail(client.user)
