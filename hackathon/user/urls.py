from django.urls import path
from user.views import UserLoginView, UserRefreshView, UserCreateView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('refresh/', UserRefreshView.as_view(), name='user-refresh'),
    path('create/', UserCreateView.as_view(), name='user-create'),
]
