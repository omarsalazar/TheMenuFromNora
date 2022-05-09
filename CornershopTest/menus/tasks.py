from __future__ import absolute_import, unicode_literals
from CornershopTest.celery import app
from datetime import datetime
from CornershopTest.menus.models import Menu
from CornershopTest.menus.serializers import MenuModelSerializer
from CornershopTest.services.slack_connection import SlackService
from CornershopTest.menus.utils import create_menu_message
from CornershopTest.orders.utils import process_orders_from_messages

service = SlackService()


@app.task
def prepare_clients():
    service.get_or_create_clients()


@app.task
def send_today_menu():
    today = datetime.now().date()
    menu_data = None
    try:
        menu = Menu.objects.get(date=today)
        menu_data = MenuModelSerializer(menu).data
    except Menu.DoesNotExist:
        pass
    menu_message = create_menu_message(menu_data)
    service.send_menu_message(menu_message)


@app.task
def process_orders():  # TODO testeas esto
    messages = service.get_messages()
    process_orders_from_messages(messages)
