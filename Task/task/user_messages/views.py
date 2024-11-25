from .models import Message
from .serializers import MessageSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.

class MessageList(generics.ListCreateAPIView):
    """
    get:
    Возвращает список всех сообщений.

    post:
    Создает новое сообщение.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class MessageDelete(generics.DestroyAPIView):
    """
    delete:
    Удаляет сообщение по его ID.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )