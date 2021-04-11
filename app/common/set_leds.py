"""Determines what colours the LEDs should be set to by:

1. The LED colour values in the config file
2. The time of sunset
3. The seasonal offset in the config file

During the least summery months, a lead time of X hours (set in config) will be applied to the Night light
transition. This is due to the early sunset in winter, day colour lighting will be wanted after the
sun has set. The same will not be true in summer.

"""

from datetime import datetime

from astral import LocationInfo
from astral.sun import sun

from common.get_conf import config_data


class GetValues():
    """
    to do
    """
    def __init__(self, config_file: str = "conf") -> None:
        self.config = config_data(config_file)
        self.led_vals = self._get_led_vals()
        self.time_now = datetime.now()

    @staticmethod
    def _get_sunset(**kwargs) -> object:
        """[summary]

        Returns:
            object: [description]
        """
        location = LocationInfo(**kwargs)
        return sun(location.observer, tzinfo=location.timezone)["sunset"]

    def _add_offset(self, sunset_dt):
        """[summary]

        Args:
            sunset_dt ([type]): [description]
        """
        # DATETIME OBJECTS NOT WRITEABLE - MAKE NEW DATETIME OBJECT
        sunset_dt.hour += self.config["seasonal_offset"][sunset_dt.month - 1]
        return sunset_dt

    def _get_led_vals(self):
        """[summary]
        """
        led_vals = None
        sunset_w_offset = self._add_offset(self._get_sunset(**self.config["locale"]))
        if sunset_w_offset < self.time_now:
            led_vals = self.config["led_colours"]["day"]
        else:
            led_vals = self.config["led_colours"]["night"]

        return led_vals


class SetValues(GetValues):
    """[summary]

    Args:
        GetValues ([type]): [description]
    """
    def __init__(self):
        super().__init__()

