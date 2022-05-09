from datetime import datetime

from CornershopTest.clients.models import Clients
from CornershopTest.menus.models import Menu
from CornershopTest.services.slack import SlackService
from CornershopTest.orders.models import Orders


def process_orders_from_messages(messages: list) -> any:  # TODO testeas esto
    instructions = ""
    try:
        for message in messages:
            text = message.get("text").lower()
            user = message.get("user")
            client = Clients.objects.filter(slack_id=user).first()
            menu = Menu.objects.get(date=datetime.now().date())
            if not client:
                SlackService().get_or_create_clients()
                client = Clients.objects.filter(slack_id=user).first()
            if "," in text:
                selected_option, selected_instructions = text.split(",")
            else:
                selected_option = text
                selected_instructions = ""
            if "option" in selected_option:
                option = menu.options.filter(name__icontains=selected_option).first()
                if "instructions" in selected_instructions:
                    instructions = selected_instructions.replace("instructions:", "")
                Orders.objects.get_or_create(
                    client_id=client.id,
                    option_id=option.id,
                    instructions=instructions,
                    date=datetime.now().date(),
                )
        return True
    except Menu.DoesNotExist as e:
        raise e
