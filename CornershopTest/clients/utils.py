from CornershopTest.clients.models import Clients


def get_valid_users(users: list) -> list:
    invalid_users = ["slackbot", "noras_daily_food_deli"]
    valid_users = [
        {"username": user.get("name"), "slack_id": user.get("id")}
        for user in users
        if user.get("name") not in invalid_users
    ]
    return valid_users


def get_username_by_slack_id(slack_id: str):
    client = Clients.objects.get(slack_id=slack_id)
    if client:
        return client.username
    return False
