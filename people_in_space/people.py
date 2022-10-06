import json
import logging
import requests

logger = logging.getLogger(__name__)


def get_people_in_space() -> list:
    people = []

    try:
        response = requests.get("http://api.open-notify.org/astros.json", timeout=10)
        response.raise_for_status()

        response_json = response.json()

        if response_json.get("message") == "success":
            return response_json.get("people", [])
    except Exception as e:
        logger.error(f"Exception while attempting to retrieve people in space: {str(e)}")

    return people


def get_slack_blocks(people: list) -> list:
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":astronaut: People in Space",
                "emoji": True,
            },
        },
        {"type": "divider"},
    ]

    people_map = {}

    for data in people:
        craft = data.get("craft", "None")
        person = data.get("name", "Unknown")

        if craft not in people_map:
            people_map[craft] = [person]
        else:
            people_map[craft].append(person)

    for craft_name, people_list in people_map.items():
        fields = []

        for astronaut in people_list:
            fields.append({"type": "mrkdwn", "text": f"{astronaut}"})

        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{craft_name}*"},
                "fields": fields,
            }
        )

    return json.dumps(blocks)
