from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView, UserDeleteView


app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),
    path(
        "delete/", UserDeleteView.as_view(),
        name="user_delete"
    ),
]

