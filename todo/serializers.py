from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import ToDoList, Todo
from rest_framework import serializers

class ToDoListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=3, message="Name must have at least 3 characters."),
            MaxLengthValidator(limit_value=255, message="Name cannot exceed 255 characters.")
        ]
    )

    class Meta:
        model = ToDoList
        fields = ["id", "name", "user"]
        read_only_fields = ["user"]

class TodoSerializer(serializers.ModelSerializer):
    task = serializers.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=3, message="Task must have at least 3 characters."),
            MaxLengthValidator(limit_value=255, message="Task cannot exceed 255 characters.")
        ]
    )

    class Meta:
        model = Todo
        fields = ["id", "task", "completed", "todolist"]
        read_only_fields = ["todolist"]

    def create(self, validated_data):
        # Set completed to False by default if not provided in the request
        completed = validated_data.pop('completed', False)
        todo = super().create(validated_data)
        todo.completed = completed
        todo.save()
        return todo
