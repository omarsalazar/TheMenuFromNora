from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from CornershopTest.menus.tests.factories import MenuFactory, OptionsFactory


class TestMenuListViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/menu/"
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_get_menu_results_not_none(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.json().get("results"))

    def test_get_menu_status_200(self):
        option = OptionsFactory()
        self.menu = MenuFactory.create(date=datetime.now(), options=(option,))
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_menu_of_today(self):
        option = OptionsFactory()
        self.menu = MenuFactory.create(date=datetime.now(), options=(option,))
        response = self.client.get(self.url)
        self.assertEquals(
            response.json().get("results")[0].get("date"), str(datetime.now().date())
        )

    def test_get_no_menu(self):
        response = self.client.get(self.url)
        self.assertEquals(response.json().get("results"), [])


class TestMenuCreateViewSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/menus/"
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_create_menu_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "a")
        option = OptionsFactory()
        MenuFactory.create(date=datetime.now(), options=(option,))
        payload = {"date": datetime.now().date(), "options": []}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEquals(response.status_code, 401)

    def test_create_menu_with_same_date(self):
        option = OptionsFactory()
        MenuFactory.create(date=datetime.now(), options=(option,))
        payload = {"date": datetime.now().date(), "options": []}
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEquals(response.status_code, 400)

    def test_edit_menu(self):
        option = OptionsFactory()
        new_option = OptionsFactory()
        menu = MenuFactory.create(date=datetime.now(), options=(option,))
        payload = {"options": [new_option.id]}
        response = self.client.patch(
            reverse("menu-detail", kwargs={"pk": menu.id}), data=payload
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_menu_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "a")
        option = OptionsFactory()
        new_option = OptionsFactory()
        menu = MenuFactory.create(date=datetime.now(), options=(option,))
        payload = {"options": [new_option.id]}
        response = self.client.patch(
            reverse("menu-detail", kwargs={"pk": menu.id}), data=payload
        )
        self.assertEqual(response.status_code, 401)


class OptionModelViewSet(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/option/"
        self.user = User.objects.create_user(
            username="foo2", email="user@foo.com", password="pass"
        )
        self.url_login = reverse("login")
        self.login_data = {"username": "foo2", "password": "pass"}
        login_resp = self.client.post(self.url_login, self.login_data, format="json")
        token = login_resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_get_menu_options_results_not_none(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.json().get("results"))

    def test_edit_menu_options(self):
        option = OptionsFactory()
        payload = {
            "name": "option 1",
            "content": "Arroz, pechuga asada, agua de horchata",
        }
        response = self.client.patch(
            reverse("options-detail", kwargs={"pk": option.id}), data=payload
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_menu_options_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "a")
        option = OptionsFactory()
        payload = {
            "name": "option 1",
            "content": "Arroz, pechuga asada, agua de horchata",
        }
        response = self.client.patch(
            reverse("options-detail", kwargs={"pk": option.id}), data=payload
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_menu_options(self):
        option = OptionsFactory()
        response = self.client.delete(
            reverse("options-detail", kwargs={"pk": option.id})
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_menu_options_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "a")
        option = OptionsFactory()
        response = self.client.delete(
            reverse("options-detail", kwargs={"pk": option.id})
        )
        self.assertEqual(response.status_code, 401)

    def test_retrieve_menu_options(self):
        option = OptionsFactory()
        response = self.client.get(reverse("options-detail", kwargs={"pk": option.id}))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_menu_options_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + "a")
        option = OptionsFactory()
        response = self.client.get(reverse("options-detail", kwargs={"pk": option.id}))
        self.assertEqual(response.status_code, 401)
