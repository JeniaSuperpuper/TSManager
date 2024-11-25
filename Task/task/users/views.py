from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework import generics
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    post:
    Получение JWT-токена для аутентификации.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserView(generics.ListCreateAPIView):
    """
    get:
    Возвращает список всех пользователей.

    post:
    Создает нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UsersUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Возвращает пользователя по его ID.

    put:
    Обновляет пользователя по его ID.

    patch:
    Частично обновляет пользователя по его ID.

    delete:
    Удаляет пользователя по его ID.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer