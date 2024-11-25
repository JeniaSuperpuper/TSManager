from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_notification()

    def send_notification(self):
        channel_layer = get_channel_layer()
        print('dsfsdfdds')
        async_to_sync(channel_layer.group_send)(
            f"user_{self.owner}",
            {
                "type": "send_notification",
                "owner": self.owner,
                "title": self.title,
                "text": self.text,

            }
        )
    def __str__(self):
        return self.title