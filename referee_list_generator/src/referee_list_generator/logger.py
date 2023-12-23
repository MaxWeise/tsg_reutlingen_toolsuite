"""Implement logging mechanisms for the project.

To be able to track operations and their results, each module can use its own
logger. The functions / classes in this file can be used to setup moduleloggers

Common Usage:

    module_logger: logging.Logger = loggers.setup_logger(__file__, logging.DEBUG)

    def function_in_file(arg: int) -> bool | None:
        module_logger.info(...)
        ...

Created: 23.12.2023
@author: Max Weise
"""

import logging


def setup_logger(logger_name: str, logging_level: int) -> logging.Logger:
    """Create a logger that can be used to print messages to the screen.

    Args:
        logger_name (str): The name of the logger displayed in the terminal.
        logging_level (int): The level used to filter logging messages.

    Returns:
        A Logger object that prints the logging messages to the screen.
    """
    loggmessage_format = logging.Formatter("[%(levelname)s] - %(message)s")

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(loggmessage_format)
    logger.addHandler(console_handler)

    return logger
