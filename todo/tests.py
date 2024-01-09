from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User


class TestTodoList(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@email.com', password='password')
        self.api_client = APIClient()

    def authenticate_user(self):
        self.api_client.force_authenticate(user=self.user)

    def test_create_todolist(self):
        self.authenticate_user()

        # Create a new TodoList
        response_create = self.api_client.post(
            "/api/todolists/", {"name": "New Todo List"})
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)


    def test_update_todolist(self):
        self.authenticate_user()

        # Create a new TodoList
        response_create = self.api_client.post(
            "/api/todolists/", {"name": "New Todo List"})
        todolist_id = response_create.data["data"]["id"]

        # Update the TodoList
        response_update = self.api_client.put(
            f"/api/todolists/{todolist_id}/", {"name": "Updated Todo List"})
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)

    def test_delete_todolist(self):
        self.authenticate_user()

        # Create a new TodoList
        response_create = self.api_client.post(
            "/api/todolists/", {"name": "New Todo List"})
        todolist_id = response_create.data["data"]["id"]

        # Delete the TodoList
        response_delete = self.api_client.delete(
            f"/api/todolists/{todolist_id}/")
        self.assertEqual(response_delete.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_create_and_retrieve_todo(self):
        self.authenticate_user()

        # Create a new TodoList
        response_create_todolist = self.api_client.post(
            "/api/todolists/", {"name": "New Todo List"})
        todolist_id = response_create_todolist.data["data"]["id"]

        # Create a new Todo within the TodoList
        response_create_todo = self.api_client.post(
            f"/api/todolists/{todolist_id}/todos/", {"task": "New Task"})
        self.assertEqual(response_create_todo.status_code,
                         status.HTTP_201_CREATED)
        todo_id = response_create_todo.data["data"]["id"]

        # Retrieve the Todo using the created ID
        response_retrieve_todo = self.api_client.get(
            f"/api/todolists/{todolist_id}/todos/{todo_id}/")
        self.assertEqual(response_retrieve_todo.status_code,
                         status.HTTP_200_OK)

    def test_update_todo(self):
        self.authenticate_user()

        # Create a new TodoList
        response_create_todolist = self.api_client.post(
            "/api/todolists/", {"name": "New Todo List"})
        todolist_id = response_create_todolist.data["data"]["id"]

        # Create a new Todo within the TodoList
        response_create_todo = self.api_client.post(
            f"/api/todolists/{todolist_id}/todos/", {"task": "New Task"})
        todo_id = response_create_todo.data["data"]["id"]

        # Update the Todo
        response_update_todo = self.api_client.put(
            f"/api/todolists/{todolist_id}/todos/{todo_id}/", {"task": "Updated Task"})
        self.assertEqual(response_update_todo.status_code, status.HTTP_200_OK)

    def test_delete_todo(self):
        self.authenticate_user()

        # Create a new TodoList
        response_create_todolist = self.api_client.post(
            "/api/todolists/", {"name": "New Todo List"})
        todolist_id = response_create_todolist.data["data"]["id"]

        # Create a new Todo within the TodoList
        response_create_todo = self.api_client.post(
            f"/api/todolists/{todolist_id}/todos/", {"task": "New Task"})
        todo_id = response_create_todo.data["data"]["id"]

        # Delete the Todo
        response_delete_todo = self.api_client.delete(
            f"/api/todolists/{todolist_id}/todos/{todo_id}/")
        self.assertEqual(response_delete_todo.status_code,
                         status.HTTP_204_NO_CONTENT)
