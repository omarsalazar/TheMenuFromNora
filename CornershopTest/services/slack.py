import pytz
from datetime import datetime
from django.conf import settings
from slack import WebClient
from slack.errors import SlackApiError

from CornershopTest.clients.models import Clients
from CornershopTest.clients.utils import get_valid_users
from CornershopTest.exceptions import (
    SlackSendMessageException,
    SlackGetMessageException,
)


class SlackService:
    def __init__(self):
        self.client = WebClient(settings.SLACK_API_KEY)
        self.channel = settings.SLACK_CHANNEL_ID

    def get_or_create_clients(self):
        try:
            users = self.client.users_list()
            users = users.get("members")
            valid_users = get_valid_users(users)
            for user in valid_users:
                Clients.objects.get_or_create(
                    username=user.get("username"), slack_id=user.get("slack_id")
                )
        except SlackApiError as e:
            raise e

    def send_menu_message(self, menu: list):
        try:
            self.client.chat_postMessage(
                channel=self.channel, as_user=True, blocks=menu
            )
            return True
        except SlackApiError as e:
            raise e
        except Exception as e:
            raise SlackSendMessageException(str(e))

    def get_messages(self):
        now = datetime.now()
        start_day_timestamp = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=8,
            minute=0,
            tzinfo=pytz.timezone("America/Santiago"),
        ).timestamp()
        end_day_timestamp = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=11,
            minute=0,
            tzinfo=pytz.timezone("America/Santiago"),
        ).timestamp()

        try:
            messages = self.client.conversations_history(
                channel=self.channel,
                oldest=start_day_timestamp,
                latest=end_day_timestamp,
            ).get("messages")

            messages = [message for message in messages if message.get("user")]

            return messages

        except SlackApiError as e:
            raise e
        except Exception as e:
            raise SlackGetMessageException(str(e))
