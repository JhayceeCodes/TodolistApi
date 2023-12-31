from django.db import models
from authentication.models import User


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):      
        return self.name


class Todo(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    complete = models.BooleanField()

    def __str__(self):
        return self.task
