from rest_framework import serializers
from .models import Project, Task, Comment
from user_messages.models import Message
from task.utils import send_mail

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        project_users = validated_data.pop('project_users', [])
        project = Project.objects.create(**validated_data)
        project.project_users.set(project_users)
        # Отправка email уведомления всем пользователям проекта
        subject = 'Вас добавили в проект'
        message = f'Здравствуйте, Вас добавили в новый проект: "{project.title}".'
        from_email = 'Poklpokl12@yandex.ru'
        recipient_list = [user.email for user in project_users]  # Список email пользователей проекта
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        for user in project_users:
            Message.objects.create(
                title=f"Welcome to {project.title}",
                text=f"Hello {user.username}, welcome to the project {project.title}!",
                owner=user,
                project=project,
                task=None
            )

        return project

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        Message.objects.create(
            title=f"Вы зачислены в новый проект: '{task.project}'",
            text=f"'{task.title}' - Ваша задача",
            owner=task.executor,
            project=task.project,
            task=task
        )
        return task


    def update(self, instance, validated_data):
        # Обновляем поля задачи
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.project = validated_data.get('project', instance.project)
        instance.executor = validated_data.get('executor', instance.executor)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.term = validated_data.get('term', instance.term)
        instance.responsible_for_test = validated_data.get('responsible_for_test', instance.responsible_for_test)
        instance.save()

        # Создаем сообщение, если задача была обновлена
        Message.objects.create(
            title=f"Задача обновлена: '{instance.title}'",
            text=f"'{instance.title}' - Ваша задача была обновлена.",
            owner=instance.executor,
            project=instance.project,
            task=instance
        )

        return instance

class CommentSerializer(serializers.ModelSerializer):
    """Какой-то сериализатор для модели комментов"""
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        Message.objects.create(
            title=f"К вашей задаче оставили комментарий.'",
            text=f"К вашей задаче оставили комментарий.",
            owner=comment.task.executor,
            project=comment.task.project,
            task=comment.task
        )
        return comment
