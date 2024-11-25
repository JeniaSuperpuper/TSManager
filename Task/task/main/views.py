from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework import generics
from .models import Project, Task, Comment
# Create your views here.

from rest_framework import generics
from django.db.models import Q

class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = Project.objects.all()

        # Сортировка
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)

        # Фильтрация
        created_from = self.request.query_params.get('created_from', None)
        created_to = self.request.query_params.get('created_to', None)
        updated_from = self.request.query_params.get('updated_from', None)
        updated_to = self.request.query_params.get('updated_to', None)

        if created_from and created_to:
            queryset = queryset.filter(created__range=(created_from, created_to))
        elif created_from:
            queryset = queryset.filter(created__gte=created_from)
        elif created_to:
            queryset = queryset.filter(created__lte=created_to)

        if updated_from and updated_to:
            queryset = queryset.filter(update__range=(updated_from, updated_to))
        elif updated_from:
            queryset = queryset.filter(update__gte=updated_from)
        elif updated_to:
            queryset = queryset.filter(update__lte=updated_to)

        return queryset

class ProjectUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )

class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        queryset = Task.objects.all()

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        created_from = self.request.query_params.get('created_from', None)
        created_to = self.request.query_params.get('created_to', None)
        updated_from = self.request.query_params.get('updated_from', None)
        updated_to = self.request.query_params.get('updated_to', None)
        term_from = self.request.query_params.get('term_from', None)
        term_to = self.request.query_params.get('term_to', None)

        if created_from and created_to:
            queryset = queryset.filter(created__range=(created_from, created_to))
        elif created_from:
            queryset = queryset.filter(created__gte=created_from)
        elif created_to:
            queryset = queryset.filter(created__lte=created_to)

        if updated_from and updated_to:
            queryset = queryset.filter(update__range=(updated_from, updated_to))
        elif updated_from:
            queryset = queryset.filter(update__gte=updated_from)
        elif updated_to:
            queryset = queryset.filter(update__lte=updated_to)

        if term_from and term_to:
            queryset = queryset.filter(term__range=(term_from, term_to))
        elif term_from:
            queryset = queryset.filter(term__gte=term_from)
        elif term_to:
            queryset = queryset.filter(term__lte=term_to)

        # Сортировка
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

class TaskUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.all()

class CommentUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer