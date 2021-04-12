"""Runtime script"""

from argparse import ArgumentParser

from common.set_leds import SetValues


if __name__ == "__main__":
    parser = ArgumentParser(description="host = The IP:PORT of the host. Example: '192.168.1.2:8080'")
    parser.add_argument("host", type=str, help="IP:PORT")

    arg = parser.parse_args()
    leds = SetValues(host=arg.host)
    resp = leds.post()
    if resp["success"] is False:
        print(resp)
