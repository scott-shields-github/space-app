import requests
from dateutil import parser
from datetime import datetime, timedelta
from launch_info.constants import ROCKET_API_URL, SPACE_X_NAME
from dataclasses import dataclass

@dataclass
class LaunchData:
    launch_name: str
    owner: str
    location: str
    launch_time: list
    description: str
    fetched_time: datetime

class LaunchInfo:
    launch_cache: list = []

    def fetch_launch_data(self) -> bool:
        response: requests.Response = requests.get(ROCKET_API_URL)
        json_response: dict = response.json()
        self.launch_cache = []
        for launch in json_response['result']:
            launch["fetched_time"] = datetime.now()
            launch_data = LaunchData(
                launch['name'],
                launch['provider']['name'],
                launch['pad']['location']['name'] + " - " + launch['pad']['location']['country'],
                (launch['win_open'], launch['est_date']),
                launch['launch_description'],
                datetime.now()
            )
            self.launch_cache.append(launch_data)
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
    def get_formatted_launch_data(launch_info: LaunchData) -> str:
        ret_str: str = ""
        ret_str += f"Launch Name: {launch_info.launch_name}\n"
        ret_str += f"Owner: {launch_info.owner}\n"
        ret_str += f"Location: {launch_info.location}\n"
        if launch_info.launch_time[0]:
            launch_time: datetime = parser.parse(launch_info.launch_time[0])
            ret_str += "Planned Launch Time: " + str(launch_time) + "\n"
        elif launch_info.launch_time[1]:
            ret_str += f"Planned Launch Date: {launch_info.launch_time[1]['year']}-" \
                       f"{launch_info.launch_time[1]['month']}-{launch_info.launch_time[1]['day']}\n"

        ret_str += "Description: " + launch_info.description + "\n"

        return ret_str

    def _check_cache_freshness(self) -> bool:
        if self.launch_cache:
            if self.launch_cache[0].fetched_time:
                if datetime.now() - self.launch_cache[0].fetched_time < timedelta(hours=1):
                    return True
        return False

    @staticmethod
    def _is_spacex(launch_data: LaunchData):
        return launch_data.owner == SPACE_X_NAME


class MissingLaunchData(Exception):
    def __str__(self):
        return 'Error: MissingLaunchData'


class ImproperLaunchRequest(Exception):
    def __str__(self):
        return 'Error: ImproperLaunchRequest'
