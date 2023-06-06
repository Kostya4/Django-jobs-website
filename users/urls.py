from django.urls import path, include
from .views import *

urlpatterns = [
    path("signup/", SignUpView.as_view(), name='signup'),
    path("logout/", LogoutUserView.as_view(), name='logout'),
    path("login/", LoginUserView.as_view(), name='login'),
    path("user-profile/<int:user_id>/", UserProfile.as_view(), name='user-profile'),
]
