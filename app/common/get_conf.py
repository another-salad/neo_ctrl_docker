"""Returns the JSON conf file as a dict"""

from pathlib import Path

from json import load


def config_data(file: str = "conf") -> dict:
    """Returns the JSON config as a dict

    Args:
        file (str): The config file name (without ext).

    Returns:
        dict: A python object
    """
    full_path = Path(__file__).parent.absolute()
    with open(Path(full_path, "config", file + ".json"), "r") as conf:
        return load(conf)
