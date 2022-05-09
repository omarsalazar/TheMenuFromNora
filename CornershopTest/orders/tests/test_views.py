from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


class TestOrderModelViewSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/order/"
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_list_orders(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_list_orders_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "a")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 401)
