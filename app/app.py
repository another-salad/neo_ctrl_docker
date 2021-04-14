"""Runtime script"""
from common.set_leds import SetValues


if __name__ == "__main__":
    leds = SetValues()
    resp = leds.set_leds()
    if resp["success"] is False:
        print(resp)
