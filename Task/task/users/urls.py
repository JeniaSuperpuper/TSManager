from django.urls import path
from .views import UserView, UsersUpdate

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>', UsersUpdate.as_view())
]
