from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Todo
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class TestAllAuth(APITestCase):
    def setUp(self):
        self.registration_url = reverse("rest_register")
        self.login_url = reverse("rest_login")
        self.user_data = {
            "username": "test123",
            "email": "test123@gmail.com",
            "password1": "123321test123123321",
            "password2": "123321test123123321"
        }
        self.login_data = {
            "username": "test123",
            "password": "123321test123123321"
        }

    def test_good_registration(self):
        response = self.client.post(self.registration_url, data=self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bad_registration(self):
        bad_data = self.user_data.copy()
        bad_data["password2"] = "no"
        response = self.client.post(self.registration_url, data=bad_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        self.client.post(self.registration_url, data=self.user_data, format="json")
        response = self.client.post(self.login_url, data=self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestTasks(APITestCase):
    def setUp(self):
        self.list_tasks_url = reverse("list_create_tasks")
        self.get_task_url = reverse("task_by_id", kwargs={"pk": 1})

        self.user = User.objects.create_user(username="testuser", password="12345testuser12345")
        self.task = Todo.objects.create(title="123", description="123", user=self.user, due_date="2024-07-15")

    def test_list_tasks(self):
        response = self.client.get(self.list_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authed_list_tasks(self):
        self.client.login(username="testuser", password="12345testuser12345")

        response = self.client.get(self.list_tasks_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_authed_get_task_by_id(self):
        self.client.login(username="testuser", password="12345testuser12345")

        response = self.client.get(self.get_task_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "123")
    
    def test_authed_patch_task_by_id(self):
        self.client.login(username="testuser", password="12345testuser12345")

        response = self.client.patch(self.get_task_url, data={"title": "new_title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "new_title")
    
    def test_authed_delete_task_by_id(self):
        self.client.login(username="testuser", password="12345testuser12345")

        response = self.client.delete(self.get_task_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Todo.objects.filter(user=self.user).exists())
