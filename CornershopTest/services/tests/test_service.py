import mock
from django.test import TestCase, override_settings
from CornershopTest.clients.models import Clients

from CornershopTest.services.slack import SlackService
from slack.errors import SlackApiError


def mocked_slack_user_list(**kargs):
    return {
        "members": [
            {
                "id": "4GB601",
                "is_bot": False,
                "name": "test",
                "profile": {"real_name": "slack_test"},
            }
        ]
    }


def mocked_slack_post_message(**kwargs):
    return {
        "ok": True,
        "channel": "FDSFD3434S43",
        "ts": "1627473015.000100",
        "message": {
            "bot_id": "B029Z3ML08Y",
            "type": "message",
            "text": "test",
            "user": "U028XEW8UQN",
            "ts": "1627473015.000100",
            "team": "T02916UL0PP",
            "bot_profile": {
                "id": "B029Z3ML08Y",
                "deleted": False,
                "name": "Nora",
                "updated": 1627370441,
                "app_id": "A0291CYFTLM",
                "team_id": "T02916UL0PP",
            },
        },
    }


def mocked_slack_messages(**kwargs):
    return {
        "messages": [
            {
                "bot_id": "B029Z3ML08Y",
                "type": "message",
                "text": "option 1",
                "user": "FSAF2133",
                "ts": "1627391934.013700",
                "team": "T02916UL0PP",
            }
        ]
    }


@override_settings(SLACK_API_KEY="", SLACK_CHANNEL_ID="")
class TestSlackService(TestCase):
    def setUp(self) -> None:
        self.service = SlackService()

    @mock.patch("slack.WebClient.users_list", side_effect=mocked_slack_user_list)
    def test_get_or_create_clients_return(self, mocked_slack_user_list):
        self.service.get_or_create_clients()
        client = Clients.objects.filter().last()
        self.assertEquals(client.slack_id, "4GB601")

    def test_get_or_create_clients_return_slack_error_connection(self):
        with self.assertRaises(SlackApiError):
            self.service.get_or_create_clients()

    @mock.patch(
        "slack.WebClient.chat_postMessage", side_effect=mocked_slack_post_message
    )
    def test_send_menu_message(self, mock_slack_chat_postMessage):
        self.assertTrue(self.service.send_menu_message(menu=[]))

    def test_send_menu_message_conection_error(self):
        with self.assertRaises(SlackApiError):
            self.service.send_menu_message(menu=[])

    @mock.patch(
        "slack.WebClient.conversations_history", side_effect=mocked_slack_messages
    )
    def test_get_messages(self, mock_slack_conversations_history):
        messages = self.service.get_messages()
        self.assertEquals(messages, mocked_slack_messages().get("messages"))

    def test_get_messages_slack_error(self):
        with self.assertRaises(SlackApiError):
            self.service.get_messages()
