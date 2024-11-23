from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project, Task, Comment
from users.models import User

class ProjectViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.project1 = Project.objects.create(title='Project 1', description='Description 1')
        self.project2 = Project.objects.create(title='Project 2', description='Description 2')



    def test_list_projects(self):
        """
        Тестирование получения списка проектов.
        """
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_project(self):
        """
        Тестирование создания нового проекта.
        """
        url = reverse('project-list')
        data = {
            'title': 'New Project',
            'description': 'New Description',
            'status': 'AC',
            'project_users': [self.user.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(Project.objects.get(id=response.data['id']).title, 'New Project')

    def test_update_project(self):
        """
        Тестирование обновления существующего проекта.
        """
        url = reverse('project-detail', args=[self.project1.id])
        data = {
            'title': 'Updated Project',
            'description': 'Updated Description',
            'status': 'AR',
            'project_users': [self.user.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.title, 'Updated Project')
        self.assertEqual(self.project1.status, 'AR')

    def test_delete_project(self):
        """
        Тестирование удаления проекта.
        """
        url = reverse('project-detail', args=[self.project1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 1)

    def test_filter_projects_by_date(self):
        """
        Тестирование фильтрации проектов по дате создания.
        """
        url = reverse('project-list')
        response = self.client.get(url, {'created_from': '2023-01-01', 'created_to': '2024-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_sort_projects_by_title(self):
        """
        Тестирование сортировки проектов по названию.
        """
        url = reverse('project-list')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Project 1')
        self.assertEqual(response.data[1]['title'], 'Project 2')

    def test_sort_projects_by_created_date(self):
        """
        Тестирование сортировки проектов по дате создания.
        """
        url = reverse('project-list')
        response = self.client.get(url, {'ordering': 'created'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Project 1')
        self.assertEqual(response.data[1]['title'], 'Project 2')

    def test_sort_projects_by_updated_date(self):
        """
        Тестирование сортировки проектов по дате обновления.
        """
        url = reverse('project-list')
        response = self.client.get(url, {'ordering': 'update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Project 1')
        self.assertEqual(response.data[1]['title'], 'Project 2')


class TaskViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(title='Test Project', description='Test Description')

        self.task1 = Task.objects.create(
            title='Task 1',
            description='Description 1',
            project=self.project,
            executor=self.user,
            term='2023-12-31',
            responsible_for_test='Tester 1'
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Description 2',
            project=self.project,
            executor=self.user,
            term='2023-12-31',
            responsible_for_test='Tester 2'
        )

    def test_list_tasks(self):
        """
        Тестирование получения списка задач.
        """
        url = reverse('task-list', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        """
        Тестирование создания новой задачи.
        """
        url = reverse('task-list', args=[self.project.id])
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'project': self.project.id,
            'executor': self.user.id,
            'term': '2023-12-31',
            'responsible_for_test': 'Tester 3'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, 'New Task')

    def test_update_task(self):
        """
        Тестирование обновления существующей задачи.
        """
        url = reverse('task-detail', args=[self.task1.id])
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'project': self.project.id,
            'executor': self.user.id,
            'term': '2023-12-31',
            'responsible_for_test': 'Tester 1'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_delete_task(self):
        """
        Тестирование удаления задачи.
        """
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_filter_tasks_by_date(self):
        """
        Тестирование фильтрации задач по дате создания.
        """
        url = reverse('task-list', args=[self.project.id])
        response = self.client.get(url, {'created_from': '2023-01-01', 'created_to': '2023-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Предполагается, что обе задачи созданы в указанном диапазоне

    def test_sort_tasks_by_title(self):
        """
        Тестирование сортировки задач по названию.
        """
        url = reverse('task-list', args=[self.project.id])
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Task 1')
        self.assertEqual(response.data[1]['title'], 'Task 2')

    def test_sort_tasks_by_created_date(self):
        """
        Тестирование сортировки задач по дате создания.
        """
        url = reverse('task-list', args=[self.project.id])
        response = self.client.get(url, {'ordering': 'created'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Task 1')
        self.assertEqual(response.data[1]['title'], 'Task 2')

    def test_sort_tasks_by_updated_date(self):
        """
        Тестирование сортировки задач по дате обновления.
        """
        url = reverse('task-list', args=[self.project.id])
        response = self.client.get(url, {'ordering': 'update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Task 1')
        self.assertEqual(response.data[1]['title'], 'Task 2')


class CommentViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(title='Test Project', description='Test Description')

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            project=self.project,
            executor=self.user,
            term='2024-12-31',
            responsible_for_test='Tester'
        )

        self.comment1 = Comment.objects.create(
            name='Comment 1',
            body='Body 1',
            task=self.task
        )
        self.comment2 = Comment.objects.create(
            name='Comment 2',
            body='Body 2',
            task=self.task
        )

    def test_list_comments(self):
        """
        Тестирование получения списка комментариев.
        """
        url = reverse('comment-list-by-task', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_comment(self):
        """
        Тестирование создания нового комментария.
        """
        url = reverse('comment-list-by-task', args=[self.task.id])
        data = {
            'name': 'New Comment',
            'body': 'New Body',
            'task': self.task.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        self.assertEqual(Comment.objects.get(id=response.data['id']).name, 'New Comment')

    def test_update_comment(self):
        """
        Тестирование обновления существующего комментария.
        """
        url = reverse('comment-detail', args=[self.comment1.id])
        data = {
            'name': 'Updated Comment',
            'body': 'Updated Body',
            'task': self.task.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.name, 'Updated Comment')

    def test_delete_comment(self):
        """
        Тестирование удаления комментария.
        """
        url = reverse('comment-detail', args=[self.comment1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)

    def test_filter_comments_by_date(self):
        """
        Тестирование фильтрации комментариев по дате создания.
        """
        url = reverse('comment-list-by-task', args=[self.task.id])
        response = self.client.get(url, {'created_from': '2023-01-01', 'created_to': '2023-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_sort_comments_by_name(self):
        """
        Тестирование сортировки комментариев по имени.
        """
        url = reverse('comment-list-by-task', args=[self.task.id])
        response = self.client.get(url, {'ordering': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Comment 1')
        self.assertEqual(response.data[1]['name'], 'Comment 2')

    def test_sort_comments_by_created_date(self):
        """
        Тестирование сортировки комментариев по дате создания.
        """
        url = reverse('comment-list-by-task', args=[self.task.id])
        response = self.client.get(url, {'ordering': 'create'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Comment 1')
        self.assertEqual(response.data[1]['name'], 'Comment 2')

    def test_sort_comments_by_updated_date(self):
        """
        Тестирование сортировки комментариев по дате обновления.
        """
        url = reverse('comment-list-by-task', args=[self.task.id])
        response = self.client.get(url, {'ordering': 'update'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Comment 1')
        self.assertEqual(response.data[1]['name'], 'Comment 2')