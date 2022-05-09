from datetime import datetime, timedelta
from django.test import TestCase
from CornershopTest.clients.tests.factories import ClientFactory
from CornershopTest.menus.tests.factories import MenuFactory, OptionsFactory
from CornershopTest.orders.utils import process_orders_from_messages
from CornershopTest.menus.models import Menu


class OrdersUtilsTestCase(TestCase):
    def setUp(self):
        self.client = ClientFactory(slack_id="DDFF")
        self.option = OptionsFactory(name="Option 1, ")

    def test_process_orders_from_messages(self):
        MenuFactory.create(date=datetime.now(), options=(self.option,))
        menu_data = [{"text": f"{self.option.name}", "user": self.client.slack_id}]
        self.assertTrue(process_orders_from_messages(messages=menu_data))

    def test_process_orders_from_messages_failed(self):
        MenuFactory.create(
            date=datetime.now() - timedelta(days=2), options=(self.option,)
        )
        menu_data = [{"text": f"{self.option.name}", "user": self.client.slack_id}]
        with self.assertRaises(Menu.DoesNotExist):
            self.assertTrue(process_orders_from_messages(messages=menu_data))
