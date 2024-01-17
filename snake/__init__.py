import os
import pathlib

from skriba.logger import setup_logger

from .viper import ascii_snake
from .viper import SnakeObject

if not os.getenv("SKRIBA_LOGGER_NAME"):
    os.environ["SKRIBA_LOGGER_NAME"] = "viper-logger"
    setup_logger(
        logger_name="viper-logger",
        log_to_term=True,
        log_to_file=False,
        log_file="viper-log-file",
        log_level="DEBUG",
    )

if pathlib.Path(__file__).parent.resolve().joinpath("config").exists():
    # If environment variable not set
    if not os.environ.get("AUROR_CONFIG_PATH"):
        os.environ["AUROR_CONFIG_PATH"] = str(pathlib.Path(__file__).parent.resolve().joinpath("config"))

    # If the environment variable does exist and is not in the list, append it
    else:
        if str(pathlib.Path(__file__).parent.resolve().joinpath("config")) not in os.environ["AUROR_CONFIG_PATH"]:
            os.environ["AUROR_CONFIG_PATH"] = os.environ["AUROR_CONFIG_PATH"] + \
                                              ":" + str(pathlib.Path(__file__).parent.resolve().joinpath("config"))

