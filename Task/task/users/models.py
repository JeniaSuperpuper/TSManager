from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Project

# Create your models here.
class User(AbstractUser):

    class Role(models.TextChoices):
        INTERN = 'IN', 'Intern'
        FRONTEND = 'FR', 'Frontend'
        BACKEND = 'BK', 'Backend'
        DEVOPS = 'DO', 'Devops'
        PROJECT_MANAGER = 'PM', 'Project_Manager'
        ANALYST = 'AN', "Analyst"
        DESIGNER = 'DS', 'Designer'

    email = models.EmailField(default='')
    usable_password = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(upload_to=None, height_field=None, null=True, blank=True)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.INTERN, null=True)
    user_projects = models.ManyToManyField(Project, null=True, blank=True)

    def __str__(self):
        return self.username


