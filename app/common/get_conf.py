"""Returns the JSON conf file as a Python object"""

from pathlib import Path

from collections import namedtuple

from json import load


def config_data(file="conf") -> object:
    """Returns the JSON config as a Python object

    Args:
        file (str, optional): The config file name (without ext). Defaults to "conf".

    Returns:
        object: A python object
    """
    full_path = Path(__file__).parent.absolute()
    with open(Path(full_path, "config", file + ".json"), "r") as conf:
        return load(conf, object_hook=lambda d: namedtuple('config', d.keys())(*d.values()))
