import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# image_module imports
from image_module.images import jwst_get_random_image_from_library, nasa_astronomy_picture_of_the_day

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

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
        }
    ]
    respond(blocks=blocks)


@app.action("apod")
def astronomy_picture_of_the_day(ack, say):
    ack()
    message = nasa_astronomy_picture_of_the_day()
    say(message)


@app.message("webb")
def random_webb_image(say):
    url = jwst_get_random_image_from_library()
    say(f"{url}")


@app.message("launches")
def launch_info(say):
    say("Upcoming rocket launches: ")


if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()