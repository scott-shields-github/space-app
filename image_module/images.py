import requests
from typing import List
from random import randrange

from image_module.constants import JWSTAPI_API_KEY, \
    JWSTAPI_IMAGE_TYPE_JPG, \
    JWSTAPI_BASE_URL, \
    JWST_SUFFIX, \
    NASA_APOD_URL, \
    NASA_IMAGE_API_KEY

jwst_headers = {"X-API-KEY": JWSTAPI_API_KEY}


# Get all James Webb Space Telescope images from https://jwstapi.com/
def jwst_get_all_jpg_images():
    image_list: List = []
    try:
        response = requests.get(f"{JWSTAPI_BASE_URL}/all/type/{JWSTAPI_IMAGE_TYPE_JPG}", headers=jwst_headers).json()
        body = response['body']
        for x in body:
            details = x['details']
            # Parse out just the full size 2D images and create a list
            if details['suffix'] == JWST_SUFFIX:
                image_list.append({"url": x['location'], "thumbnail": x['thumbnail']})
        for x in image_list:
            print(x)
        return body
    except Exception as e:
        print(e)


def jwst_get_random_image_from_library():
    image_urls: List = []
    random_selection = randrange(len(image_urls))
    image_to_send = image_urls[random_selection]['url']


def nasa_astronomy_picture_of_the_day(date: str = None):
    params = {
        "api_key": NASA_IMAGE_API_KEY,
        "date": date
    } if date else {"api_key": NASA_IMAGE_API_KEY}
    print(params)
    try:
        body = requests.get(NASA_APOD_URL, params=params).json()
        if body['media_type'] != "image":
            result = f"No image results available for date: {body['date']}"
        title = body['title']
        description = body['explanation']
        hdurl = body['hdurl']
        url = body['url']
        copyright = body['copyright']
        return
    except Exception as e:
        print(e)
