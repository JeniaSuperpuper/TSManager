from django.urls import path, include
from users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import *


urlpatterns = [
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/projects/', ProjectView.as_view()),
    path('api/v1/projects/<int:pk>/', ProjectUpdate.as_view()),
    path('api/v1/projects/<int:project_id>/tasks/', TaskView.as_view()),
    path('api/v1/tasks/', TaskView.as_view()),
    path('api/v1/tasks/<int:pk>/', TaskUpdate.as_view()),
    path('api/v1/comments/', CommentView.as_view()),
    path('api/v1/comments/<int:pk>/', CommentUpdate.as_view()),
    path('api/v1/tasks/<int:task_id>/comments/', CommentView.as_view()),

    path('api/v1/users/', include('users.urls')),

    path('api/v1/messages/', include('user_messages.urls')),
]
