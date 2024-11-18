from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework import generics
from .models import Project, Task, Comment
# Create your views here.

class ProjectView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class ProjectUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )


class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()



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