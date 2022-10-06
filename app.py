import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from launch_info import LaunchInfo, LaunchData

# image_module imports
from image_module.images import jwst_get_random_image_from_library, nasa_astronomy_picture_of_the_day

from people_in_space.people import get_people_in_space, get_slack_blocks

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])
launch_info_obj: LaunchInfo = LaunchInfo()
# Add functionality here
@app.command("/space")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Random James Webb Image",
                    },
                    "value": "random_webb",
                    "action_id": "random_webb"
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Rocket Launch Info",
                    },
                    "value": "launch",
                    "action_id": "launch_info"
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "NASA Image of the Day",
                    },
                    "value": "apod",
                    "action_id": "apod"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Select a Specific Date for a NASA Astronomy Image of the Day"
            },
            "accessory": {
                "type": "datepicker",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date"
                },
                "action_id": "datepicker-apod"
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Who's in Space?",
                    },
                    "value": "pis",
                    "action_id": "pis"
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "See Upcoming Rocket launches",
                    },
                    "value": "launches",
                    "action_id": "launches"
                }
            ]
        }
    ]
    respond(blocks=blocks)


@app.action("apod")
def astronomy_picture_of_the_day(ack, say):
    ack()
    message_blocks = nasa_astronomy_picture_of_the_day()
    say(blocks=message_blocks)

@app.action("pis")
def people_in_space(ack, say):
  ack()
  say(blocks=get_slack_blocks(get_people_in_space()))

@app.action("random_webb")
def random_webb_image(ack, say):
    ack()
    url = jwst_get_random_image_from_library()
    say(f"A random James Webb image for your viewing pleasure\n{url}")

@app.message("launches")
def launch_info(say):
    say("Upcoming rocket launches: ")


@app.action("datepicker-apod")
def date_selection_apod(ack, say, payload):
    ack()
    message_blocks = nasa_astronomy_picture_of_the_day(payload["selected_date"])
    say(blocks=message_blocks)


@app.message("apod")
def apod_tester(say):
    say(blocks=[{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Select a Specific Date for a NASA Astronomy Image of the Day"
        },
        "accessory": {
            "type": "datepicker",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a date"
            },
            "action_id": "datepicker-apod"
        }
    }])


@app.message("launches")
def launch_info(say):
    say("Upcoming rocket launches: ")


@app.action("launches")
def launch_info(ack, say):
    ack()
    ret_str: str = ""
    for launch in launch_info_obj.get_next_launch(1):
        ret_str += launch_info_obj.get_formatted_launch_data(launch) + "\n"
    say(ret_str)

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
