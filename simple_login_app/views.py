from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import traceback
import logging
from simple_login_app.models import UserTypes
from simple_login_app.services.user.authentication import UserAuth
from simple_login_app.services.user.user import UserService, ClientService
from simple_login_app.utils import log_error_traceback

logger = logging.getLogger(__name__)


class Health(APIView):

    def get(self):
        res = {
            'healthy': 'true'
        }
        return Response(res, status=status.HTTP_200_OK)





class CreateUser(APIView):

    def post(self, request):
        try:
            data = request.data
            user = UserService.create_user(data)
            if user:
                return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error while creating the milestone details{log_error_traceback(e, traceback)}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            user_type = data.get('user_type')
            logger.info(f'User login request : user - {username}, user_type - {user_type}')
            user = UserAuth.authenticate(username, password)
            if user:
                user_details = {
                    'first_name': user.firstname,
                    'is_active': user.is_active,
                    'role': user.role,
                    'last_login': user.last_login,
                    'user_type': user_type
                }
                if user_type == UserTypes.CLIENT.lower():
                    user_details['fullname'] = data.get('fullname')
                    user_details['companyname'] = data.get('companyname')
                    ClientService.update_client_login(username)
                return Response(user_details, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f'Error while creating the milestone details{log_error_traceback(e, traceback)}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = request.data
            username = data.get('username')
            client = ClientService.get_client(username)
            return Response(client, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error while creating the milestone details{log_error_traceback(e, traceback)}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientDashboard(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            req_params = request.query_params
            username = req_params.get('username')
            client = ClientService.get_client(username)
            return Response(client.json(), status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error while creating the milestone details{log_error_traceback(e, traceback)}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AdminDashboard(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        try:
            req_params = request.query_params
            username = req_params.get('username')
            user = UserService.get_user(username)
            return Response(user, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error while creating the milestone details{log_error_traceback(e, traceback)}')
            return Response(status=status.HTTP_400_BAD_REQUEST)



