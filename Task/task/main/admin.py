from django.contrib import admin
from .models import Project, Task, Comment

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'status', 'created', 'update'   ]
    list_editable = ['status']


admin.site.register(Task)
admin.site.register(Comment)