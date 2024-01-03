from django.urls import path
from . import views

urlpatterns = [
    path("todolists/",views.ToDoListView.as_view()),
    path("todolists/<int:pk>", views.ToDoListDetailView.as_view()),
    path("todolists/<int:todolist_id>/todos/", views.TodoView.as_view()),
    path("todolists/<int:todolist_id>/todos/<int:pk>", views.TodoDetailView.as_view()),
]
