from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [

    url(r'^api/token/', jwt_views.TokenObtainPairView.as_view()),
    url(r'^api/token/refresh/', jwt_views.TokenRefreshView.as_view()),
    url(r'^health', views.Health.as_view()),
    url(r'^create-user', views.CreateUser.as_view()),
    url(r'^login', views.UserLogin.as_view()),
    url(r'^client-auth', views.ClientAuth.as_view()),
    url(r'^dashboard', views.ClientDashboard.as_view()),
    url(r'^admin-dashboard', views.AdminDashboard.as_view()),
]
