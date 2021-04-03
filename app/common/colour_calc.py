"""Determines what colours the LEDs should be set to by:

1. The LED colour values in the config file
2. The time of sunset
3. The seasonal variance in the config file

During the least summery months, a lead time of X hours (set in config) will be applied to the Night light
transition. This is due to the early sunset in winter, day colour lighting will be wanted after the
sun has set. The same will not be true in summer.

"""


from astral import LocationInfo
from astral.sun import sun

