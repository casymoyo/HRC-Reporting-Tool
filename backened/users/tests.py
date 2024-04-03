from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_creation_valid_data(self):
        data = {
            "username": "casy",
            "email": "casy@example.com",
            "password": "1234567",
        }
        response = self.client.post("/users/register/", data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_user_creation_invalid_email(self):
        data = {
            "username": "casy",
            "email": "invalid_email",
            "password": "secretpassword",
        }
        response = self.client.post("/users/register/", data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_user_login_correct_credentials(self):
        user = User.objects.create_user(
            username="casper", email="casy@email.com", password="secretpassword"
        )
        response = self.client.post("/users/login/", data={"username": "casper", "password": "secretpassword"})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue("tokens" in response.data)

    def test_user_login_incorrect_credentials(self):
        User.objects.create_user(
            username="casper", email="casy@example.com", password="secretpassword"
        )
        response = self.client.post("/users/login/", data={"username": "johndoe", "password": "wrongpassword"})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_user_details_valid_token(self):
        user = User.objects.create_user(
            username="casper", email="casy@example.com", password="secretpassword"
        )
        token = RefreshToken.for_user(user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/users/users/")
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_user_details_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Invalid Token")
        response = self.client.get("users-detail")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

