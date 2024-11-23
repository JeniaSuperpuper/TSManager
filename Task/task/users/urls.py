from django.urls import path
from .views import UserView, UsersUpdate

urlpatterns = [
    path('', UserView.as_view(), name='user-list'),
    path('<int:pk>/', UsersUpdate.as_view(), name='user-detail')
]
