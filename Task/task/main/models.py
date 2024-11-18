from django.db import models

# Create your models here.

class Project(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        ARCHIVE = 'AR', 'Archive'

    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    project_users = models.ManyToManyField("users.User")

    def __str__(self):
        return self.title

class Task(models.Model):

    class Status(models.TextChoices):
        GROOMING = 'GR', 'Grooming'
        IN_PROGRESS = 'IP', 'In Progress'
        DEV = 'DV', 'Dev'
        DONE = 'DN', 'Done'

    class Priority(models.TextChoices):
        LOW = 'LW', 'Low'
        AVERAGE = 'AR', 'Average'
        HIGH = 'HG', 'High'

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    executor = models.ForeignKey("users.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.GROOMING)
    priority = models.CharField(max_length=2, choices=Priority.choices, default=Priority.LOW)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    term = models.DateField()
    responsible_for_test = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    create = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

