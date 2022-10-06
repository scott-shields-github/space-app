import requests
import logging
from typing import Optional, Tuple
from requests.exceptions import HTTPError
from math import radians, sin, cos, asin, sqrt
from iss_constants import ISS_NOW_URL, IPINFO_URL, RADIUS, EARTH_RADIUS
from geopy.geocoders import Nominatim

_logger = logging.getLogger(__name__)


def get_current_ISS_coordinates() -> Optional[Tuple]:
    """
    :returns: A tuple with (latitude, longitude) information of the ISS
    """
    try:
        response = requests.get(ISS_NOW_URL)

        if not response.status_code == 200:
            return None

        data = response.json()

        iss_position = data.get("iss_position", {})

        if not iss_position:
            return None

        return float(iss_position.get("latitude")), float(iss_position.get("longitude"))

    except HTTPError as e:
        _logger.exception(f"HTTPError while getting ISS coordinates: {e}")
    except Exception as e:
        _logger.exception(f"Failed getting ISS coordinates: {e}")

    return None


def get_user_current_coordinates() -> Optional[Tuple]:
    """
    :returns: A tuple with user's current coordinates in
    """
    try:
        response = requests.get(IPINFO_URL)

        if not response.status_code == 200:
            return None

        data = response.json()
        user_location = data.get("loc", "")
        lat, long = user_location.split(",")

        return float(lat), float(long)

    except HTTPError as e:
        _logger.exception(f"HTTPError while getting user's coordinates: {e}" )

    except Exception as e:
        _logger.exception(f"Failed getting user's coordinates: {e}")

    return None


def is_iss_in_radius(user_latitude, user_longitude, iss_latitude, iss_longitude) -> bool:
    """
    Determine if the ISS is within a certain radius
    This will allow the sighting of the ISS even if the ISS is not exactly on your coordinates
    Leaves some room for error

    Currently, considering a 5mile radius from the user's location.

    :param user_latitude:
    :param user_longitude:
    :param iss_latitude:
    :param iss_longitude:
    :return: Boolean depending on whether the ISS lies within the 5 mile radius of the user
    """
    distance = _calculate_haversine_distance(user_longitude, user_latitude, iss_longitude, iss_latitude)
    return distance < RADIUS


def _calculate_haversine_distance(lon1, lat1, lon2, lat2):
    """
    Calculate distance of two locations on a sphere.
    Reference: https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97

    :returns: Distance between two coordinates in miles
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    return 2 * EARTH_RADIUS * asin(sqrt(a))


def current_location_of_iss() -> str:
    iss_lat, iss_long = get_current_ISS_coordinates()
    coordinates = str(iss_lat) + "," + str(iss_long)
    geoLoc = Nominatim(user_agent="GetLoc")
    location = geoLoc.reverse(coordinates)
    return location.address if location is not None else ""

