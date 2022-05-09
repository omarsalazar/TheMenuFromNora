from typing import Optional
from django.conf import settings


def create_menu_message(menu_data: Optional[dict]) -> list:
    data = [
        {
            "type": "section",
            "text": {"type": "plain_text", "text": "Hi, good morning!"},
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Here's the menu for today: ",
            },
        },
    ]
    if menu_data:
        for menu in menu_data["options"]:
            data.append(
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"-> {menu.get('name')}: {menu.get('content')}",
                    },
                }
            )

        data.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"You can see today's menu here: {settings.HOST}/api/v1/menu/{menu_data.get('id')}",
                },
            }
        )
    else:
        data.append(
            {
                "type": "section",
                "text": {"type": "plain_text", "text": "-> no menu today, yet"},
            }
        )
    data.append(
        {
            "type": "section",
            "text": {"type": "plain_text", "text": "Have a nice one ;)"},
        }
    )
    return data
