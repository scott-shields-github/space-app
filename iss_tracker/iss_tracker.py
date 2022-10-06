# Poll every 30 secs,
# If ISS falls in radius, then set alert_flag & timeout_flag to True
# Send alert if  alert_flag & timeout_flag is true, reset the alert_flag to False
# Reset the timeout_flag after 5 mins

import iss_tracker.iss_utils as utils
from threading import Thread, Timer
from time import sleep
import logging

logging.basicConfig()


class ISSTracker:

    def __init__(self):
        self.user_latitude, self.user_longitude = utils.get_user_current_coordinates()
        self.timeout_flag = True
        self.alert_flag = False

    def check_for_iss(self):
        """
        Target for running a thread continuously to monitor the ISS
        """
        while True:
            iss_lat, iss_long = utils.get_current_ISS_coordinates()
            # iss_lat, iss_long = 37.385414681834746,-122.01427335010969 #  TODO: Delete test case
            if utils.is_iss_in_radius(self.user_latitude, self.user_longitude, iss_lat, iss_long):
                self.alert_flag = True
                if self.alert_flag and self.timeout_flag:
                    self._send_alert()
                    Timer(300, self._reset_timeout_flag).start()
                sleep(30)

    def _send_alert(self):
        # Send alert with whatever method we choose
        self.timeout_flag = False
        print("Lookup in the sky my dude")

    def _reset_timeout_flag(self):
        self.timeout_flag = True
        return

    def start_tracking(self):
        tracker_thread = Thread(target=self.check_for_iss, name='tracker_thread')
        tracker_thread.start()
