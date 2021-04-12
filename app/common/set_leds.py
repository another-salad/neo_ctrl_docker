"""Determines what colours the LEDs should be set to by:

1. The LED colour values in the config file
2. The time of sunset/sunrise
3. The seasonal offset in the config file

During the least summery months, a lead time of X hours (set in config) will be applied to the night light
transition. This is due to the early sunset in winter, day colour lighting will be wanted after the
sun has set. The same will not be true in summer.

The night is deemed to have finished when the sun rises!

"""

from datetime import datetime

from pytz import timezone

from requests import post

from astral import LocationInfo
from astral.sun import sun

from common.get_conf import config_data


class ValuesBase():
    """
    to do
    """
    config = config_data()
    location = LocationInfo(**config["locale"])
    time_now = datetime.now(timezone(config["locale"]["timezone"]))

    def __init__(self) -> None:
        self.sunrise = self._get_sun("sunrise")
        self.sunset = self._get_sun("sunset")

    def _get_sun(self, key) -> object:
        """[summary]

        Args:
            key ([type]): [description]

        Returns:
            object: [description]
        """
        return sun(self.location.observer, tzinfo=self.location.timezone)[key]

    def _add_offset(self, sunset_dt):
        """[summary]

        Args:
            sunset_dt ([type]): [description]

        Returns:
            object: A Datetime object
        """
        offset_hour = sunset_dt.hour + self.config["seasonal_offset"][sunset_dt.month - 1]
        return datetime(
            year=sunset_dt.year,
            month=sunset_dt.month,
            day=sunset_dt.day,
            hour=offset_hour,
            minute=sunset_dt.minute,
            tzinfo=sunset_dt.tzinfo
        )

    def _get_led_vals(self):
        """[summary]
        """
        led_vals = None
        sunset_w_offset = self._add_offset(self.sunset)
        if sunset_w_offset > self.time_now > self.sunrise:
            led_vals = self.config["led_colours"]["day"]
        else:
            led_vals = self.config["led_colours"]["night"]

        return led_vals


class SetValues(ValuesBase):
    """[summary]

    Args:
        GetValues ([type]): [description]
    """
    def __init__(self, host) -> None:
        super().__init__()
        self.host = host
        self.led_vals = self._get_led_vals()

    def post(self, page="set_all", vals=None):
        """posts the LED values"""
        if not vals:
            vals = self.led_vals

        try:

            resp = post(f"http://{self.host}/{page}", json=vals)
            resp = resp.json()
        
        except Exception as ex:
            resp = {"success": False, "error": str(ex), "time": self.time_now.strftime("%d/%m/%Y, %H:%M:%S")}

        return resp
