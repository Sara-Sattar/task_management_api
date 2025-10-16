from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, TaskCompleteView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('tasks/<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
]
