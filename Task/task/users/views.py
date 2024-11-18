from .serializers import UserSerializer
from rest_framework import generics
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerializer

class UsersUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
