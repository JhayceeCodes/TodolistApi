from .models import ToDoList, Todo
from rest_framework.serializers import ModelSerializer

class ToDoListSerializer(ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ["id", "name"]
