from .models import Message
from .serializers import MessageSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class MessageDelete(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )