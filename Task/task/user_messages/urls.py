from django.urls import path
from .views import MessageList, MessageDelete

urlpatterns = [
    path('', MessageList.as_view()),
    path('delete/<int:pk>', MessageDelete.as_view())
]