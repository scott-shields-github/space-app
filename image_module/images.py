import requests
from random import randrange

from image_module.constants import NASA_APOD_URL, NASA_IMAGE_API_KEY

from image_module.jwst_image_library import image_urls


def jwst_get_random_image_from_library():
    random_selection = randrange(len(image_urls))
    image_to_send = image_urls[random_selection]['url']
    return image_to_send


def nasa_astronomy_picture_of_the_day(date: str = None):
    params = {
        "api_key": NASA_IMAGE_API_KEY,
        "date": date
    } if date else {"api_key": NASA_IMAGE_API_KEY}
    try:
        body = requests.get(NASA_APOD_URL, params=params).json()
        print(body)
        title = body['title']
        description = body['explanation']
        url = body['url']
        date = body['date']
        copyright = body['copyright'] if body['copyright'] else "Unattributed"
        message_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "NASA Astronomy Image of the Day"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"Picture of the day from {date}"
                    }
                ]
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": f"{title}"
                },
                "image_url": f"{url}",
                "alt_text": f"{title}"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"Copyright: {copyright}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{description}"
                }
            }
        ]
        return message_blocks
    except Exception as e:
        return e
