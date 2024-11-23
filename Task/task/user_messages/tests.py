from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Message
from users.models import User
from main.models import Project, Task

class MessageViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(title='Test Project', description='Test Description')

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            project=self.project,
            executor=self.user,
            term='2023-12-31',
            responsible_for_test='Tester'
        )

        # Создание тестовых сообщений
        self.message1 = Message.objects.create(
            title='Message 1',
            text='Text 1',
            owner=self.user,
            project=self.project,
            task=self.task
        )
        self.message2 = Message.objects.create(
            title='Message 2',
            text='Text 2',
            owner=self.user,
            project=self.project,
            task=self.task
        )

    def test_list_messages(self):
        """
        Тестирование получения списка сообщений.
        """
        url = reverse('message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_message(self):
        """
        Тестирование создания нового сообщения.
        """
        url = reverse('message-list')
        data = {
            'title': 'New Message',
            'text': 'New Text',
            'owner': self.user.id,
            'project': self.project.id,
            'task': self.task.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(Message.objects.get(id=response.data['id']).title, 'New Message')

    def test_delete_message(self):
        """
        Тестирование удаления сообщения.
        """
        url = reverse('message-delete', args=[self.message1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 1)

    def test_filter_messages_by_owner(self):
        """
        Тестирование фильтрации сообщений по владельцу.
        """
        url = reverse('message-list')  # Замените 'message-list' на ваш фактический URL-именованный маршрут
        response = self.client.get(url, {'owner': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Предполагается, что оба сообщения принадлежат тестовому пользователю

    def test_filter_messages_by_project(self):
        """
        Тестирование фильтрации сообщений по проекту.
        """
        url = reverse('message-list')  # Замените 'message-list' на ваш фактический URL-именованный маршрут
        response = self.client.get(url, {'project': self.project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Предполагается, что оба сообщения принадлежат тестовому проекту

    def test_filter_messages_by_task(self):
        """
        Тестирование фильтрации сообщений по задаче.
        """
        url = reverse('message-list')  # Замените 'message-list' на ваш фактический URL-именованный маршрут
        response = self.client.get(url, {'task': self.task.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Предполагается, что оба сообщения принадлежат тестовой задаче

    def test_sort_messages_by_title(self):
        """
        Тестирование сортировки сообщений по заголовку.
        """
        url = reverse('message-list')  # Замените 'message-list' на ваш фактический URL-именованный маршрут
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Message 1')
        self.assertEqual(response.data[1]['title'], 'Message 2')

    def test_sort_messages_by_created_date(self):
        """
        Тестирование сортировки сообщений по дате создания.
        """
        url = reverse('message-list')  # Замените 'message-list' на ваш фактический URL-именованный маршрут
        response = self.client.get(url, {'ordering': 'created'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Message 1')
        self.assertEqual(response.data[1]['title'], 'Message 2')