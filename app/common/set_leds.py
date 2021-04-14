"""Determines what colours the LEDs should be set to by:

1. The LED colour values in the config file
2. The time of sunset/sunrise
3. The seasonal offset in the config file
4. The LDR edge time - (i.e the brightness in the room)

During the least summery months, a lead time of X hours (set in config) will be applied to the night light
transition. This is due to the early sunset in winter, day colour lighting will be wanted after the
sun has set. The same will not be true in summer.

A 'quiet time' can also be set, meaning no LED lights will be on during these hours, regardless of brightness, etc.

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
        self.led_host = self.config["hosts"]["led"]
        self.led_vals = self._get_led_conf_vals()

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

    def _get_led_conf_vals(self):
        """[summary]
        """
        led_vals = None
        sunset_w_offset = self._add_offset(self.sunset)
        if not self._leds_on():
            led_vals = self.config["led_colours"]["off"]
        elif sunset_w_offset > self.time_now > self.sunrise:
            led_vals = self.config["led_colours"]["day"]
        else:
            led_vals = self.config["led_colours"]["night"]

        return led_vals

    def _leds_on(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return_val = False
        ldr_host = self.config["hosts"]["ldr"]
        ldr_page = self.config["ldr_page"]
        ldr_wait_time = self.config["ldr_time"]  # how long the LDR edge time should take before allowing the LEDS to turn on
        quiet_time = self.config["quiet_time"]
        if not (quiet_time["start"] < self.time_now.strftime("%H:%M:%S") < quiet_time["end"]):  # If we are in quiet hours, lets not waste time reading an LDR edge value...
            ldr_host_resp = self._post(host=ldr_host, page=ldr_page, vals={"iterations": 2})
            if not isinstance(ldr_host_resp, dict) or "average" not in ldr_host_resp.keys():
                # add some logging here?
                print(f"Error! Returned response from LDR host: {ldr_host_resp}")
            else:
                actual_ldr_time = ldr_host_resp["average"]
                if ldr_wait_time < actual_ldr_time:
                    return_val = True

        return return_val

    def _post(self, host, page, vals):
        """[summary]

        Args:
            host ([type]): [description]
            page ([type]): [description]
            vals ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:

            resp = post(f"http://{host}/{page}", json=vals)
            resp = resp.json()

        except Exception as ex:
            resp = {"success": False, "error": str(ex), "time": self.time_now.strftime("%d/%m/%Y, %H:%M:%S")}

        return resp


class SetValues(ValuesBase):
    """[summary]

    Args:
        ValuesBase ([type]): [description]
    """
    def __init__(self) -> None:
        super().__init__()

    def set_leds(self, page="set_all"):
        """[summary]

        Args:
            page (str, optional): [description]. Defaults to "set_all".

        Returns:
            [type]: [description]
        """
        return self._post(host=self.led_host, page=page, vals=self.led_vals)
