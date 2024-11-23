from django.urls import path
from .views import MessageList, MessageDelete

urlpatterns = [
    path('', MessageList.as_view(), name='message-list'),
    path('delete/<int:pk>', MessageDelete.as_view(), name='message-delete')
]