from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django_filters import rest_framework as filters

from .models import Todo
from .serializers import TodoSerializer, TodoListSerializer

# Create your views here.

class TasksPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"

class ListTasks(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TasksPagination
    filter_backends = [filters.DjangoFilterBackend,]
    filterset_fields = ["complete", "due_date",]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

class RetrieveTask(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            task = Todo.objects.get(id=pk, user=request.user)

            ser = TodoSerializer(task)

            return Response(ser.data, status=200)
        except Todo.DoesNotExist:
            return Response({"Info": "There is no task with this id"}, status=404)
        
    def delete(self, request, pk, format=None):
        try:
            task = Todo.objects.get(id=pk, user=request.user)

            task.delete()

            return Response({"Info": "Task was deleted!"}, status=200)
        except Todo.DoesNotExist:
            return Response({"Info": "There is no task with this id"}, status=404)

    def patch(self, request, pk):
        try:
            task = Todo.objects.get(id=pk, user=request.user)

            ser = TodoSerializer(task, data=request.data, partial=True)

            if ser.is_valid():
                ser.save()
                
                return Response(ser.data, status=200)
            else:
                return Response(ser.errors, status=400)
        except ValidationError as e:
            return Response(e.error_dict, status=400)
        except Todo.DoesNotExist:
            return Response({"Info": "There is no task with this id"}, status=404)