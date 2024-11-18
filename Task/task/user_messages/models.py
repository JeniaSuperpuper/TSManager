from django.utils import timezone

from django.db import models
from users.models import User
from main.models import Project, Task
# Create your models here.

class Message(models.Model):

    title = models.CharField(max_length=150)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True  )

    def __str__(self):
        return self.title