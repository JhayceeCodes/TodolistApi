from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from core.views import BaseAPIView


class ToDoListView(ListCreateAPIView, BaseAPIView):
    pass