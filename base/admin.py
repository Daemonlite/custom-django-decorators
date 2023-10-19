from django.contrib import admin
from base.models import Task
# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'complete']