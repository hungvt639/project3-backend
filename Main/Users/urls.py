from django.conf.urls import url
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.CreateUser.as_view()),
    path('profile/', views.Profile.as_view()),
    path('change-password/', views.ChangePassword.as_view()),
    url(r'^password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('logout/', views.Logout.as_view()),
    path('change-avatar/', views.Avatar.as_view())
]