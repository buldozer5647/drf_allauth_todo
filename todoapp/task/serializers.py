from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "created_at", "due_date", "complete"]
        read_only_fields = ["id", "created_at"]

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "created_at", "due_date", "complete"]
        read_only_fields = ["id", "created_at", "complete"]
