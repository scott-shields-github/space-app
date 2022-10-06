import requests
from dateutil import parser
from datetime import datetime, timedelta

ROCKET_API_URL: str = "https://fdo.rocketlaunch.live/json/launches/next/5"


class LaunchInfo:
    launch_cache: list = []

    def fetch_launch_data(self) -> bool:
        response: requests.Response = requests.get(ROCKET_API_URL)
        json_response: dict = response.json()
        self.launch_cache = []
        for launch in json_response['result']:
            launch["fetched_time"] = datetime.now()
            self.launch_cache.append(launch)
        return len(self.launch_cache) > 1

    def get_next_launch(self, launches_total: int = 1) -> list:
        if launches_total > 5 or launches_total < 0:
            raise ImproperLaunchRequest
        if self._check_cache_freshness():
            try:
                return self.launch_cache[:launches_total]
            except IndexError:
                raise ImproperLaunchRequest
        else:
            if self.fetch_launch_data() and self.launch_cache:
                try:
                    return self.launch_cache[:launches_total]
                except IndexError:
                    raise ImproperLaunchRequest
            else:
                raise MissingLaunchData

    @staticmethod
    def get_formatted_launch_data(launch_info: dict) -> str:
        ret_str: str = ""
        ret_str += "Launch Name: " + launch_info['name'] + "\n"
        ret_str += "Owner: " + launch_info['provider']['name'] + "\n"
        ret_str += "Location: " + launch_info['pad']['location']['name'] + " - " + launch_info['pad']['location']['country'] + "\n"
        if launch_info['win_open']:
            launch_time: datetime = parser.parse(launch_info['win_open'])
            ret_str += "Planned Launch Time: " + str(launch_time) + "\n"
        elif launch_info['est_date']:
            ret_str += "Planned Launch Date: " + launch_info['est_date']['year'] + "-" + launch_info['est_date']['month'] + "-" + {launch_info['est_date']['day']} + "\n"

        ret_str += "Description: " + launch_info['launch_description'] + "\n"

        return ret_str

    def _check_cache_freshness(self) -> bool:
        if self.launch_cache:
            if self.launch_cache[0]['fetched_time']:
                if datetime.now() - self.launch_cache[0]['fetched_time'] < timedelta(hours=1):
                    return True
        return False


class MissingLaunchData(Exception):
    def __str__(self):
        return 'MissingLaunchData'


class ImproperLaunchRequest(Exception):
    def __str__(self):
        return 'ImproperLaunchRequest'
