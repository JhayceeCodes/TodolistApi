from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import ToDoList, Todo
from .serializers import ToDoListSerializer, TodoSerializer
from core.views import BaseAPIView


class ToDoListView(ListCreateAPIView, BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ToDoListSerializer


    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        custom_response = self.format_response(
            message="Todo lists fetched successfully",
            data=serializer.data    
        )
        return custom_response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        custom_response = self.format_response(
            message="Todo list created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
        return custom_response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToDoListDetailView(RetrieveUpdateDestroyAPIView, BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ToDoListSerializer
    queryset = ToDoList.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied(
                "You don't have permission to access this ToDoList.")

        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        custom_response = self.format_response(
            message="Todo list fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        return custom_response

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        custom_response = self.format_response(
            message="Todo list deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )
        return custom_response


class TodoView(ListCreateAPIView, BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self, todolist_id):
        todolist = ToDoList.objects.get(id=todolist_id)
        if not todolist.user == self.request.user:
            raise PermissionDenied(
                "You don't have permission to access this Todolist.")
        return Todo.objects.filter(todolist_id=todolist_id)

    def list(self, request, todolist_id, *args, **kwargs):
        queryset = self.get_queryset(todolist_id)
        serializer = self.serializer_class(queryset, many=True)
        custom_response = self.format_response(
            message="Todos fetched successfully",
            data=serializer.data
        )
        return custom_response

    def create(self, request, todolist_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, todolist_id)
        custom_response = self.format_response(
            message="Todo created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
        return custom_response

    def perform_create(self, serializer, todolist_id):
        serializer.save(todolist_id=todolist_id)


class TodoDetailView(RetrieveUpdateDestroyAPIView, BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_object(self):
        obj = super().get_object()
        todolist_id = self.kwargs.get('todolist_id')
        todolist = ToDoList.objects.get(id=todolist_id)
        if obj.todolist_id != todolist_id:
            raise NotFound(
                "Todo does not exist")
        elif todolist.user != self.request.user:
            raise PermissionDenied(
                "You don't have permission to access this Todo")
        else:
            return obj

    def get(self, request, todolist_id, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        custom_response = self.format_response(
            message="Todo fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        return custom_response

    def delete(self, request, todolist_id, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        custom_response = self.format_response(
            message="Todo deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )
        return custom_response