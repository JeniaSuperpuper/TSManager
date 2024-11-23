from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.client.force_authenticate(user=self.user)

        self.user1 = User.objects.create_user(username='user1', password='pass1', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='pass2', email='user2@example.com')

    def test_list_users(self):
        """
        Тестирование получения списка пользователей.
        """
        url = reverse('user-list')  # Замените 'user-list' на ваш фактический URL-именованный маршрут
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_user(self):
        """
        Тестирование создания нового пользователя.
        """
        url = reverse('user-list')  # Замените 'user-list' на ваш фактический URL-именованный маршрут
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com',
            'role': 'IN'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')

    def test_update_user(self):
        """
        Тестирование обновления существующего пользователя.
        """
        url = reverse('user-detail', args=[self.user1.id])
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'role': 'FR',
            'password': '4242342'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')
        self.assertEqual(self.user1.email, 'updateduser@example.com')

    def test_delete_user(self):
        """
        Тестирование удаления пользователя.
        """
        url = reverse('user-detail', args=[self.user1.id])  # Замените 'user-detail' на ваш фактический URL-именованный маршрут
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)

