from django.urls import path
from . import views

urlpatterns = [
    path("tasks/", views.ListTasks.as_view(), name="list_create_tasks"),
    path("tasks/<int:pk>", views.RetrieveTask.as_view(), name="task_by_id"),
]
