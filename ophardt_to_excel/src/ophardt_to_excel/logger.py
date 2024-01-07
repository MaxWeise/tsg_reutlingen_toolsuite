"""Implement logging mechanisms for the project.

To be able to track operations and their results, each module can use its own
logger. The functions / classes in this file can be used to setup moduleloggers

Common Usage:

    module_logger: logger.Logger = logger.logger_factory("console",
                                                            __name__,
                                                            logging.DEBUG)

    def function_in_file(arg: int) -> bool | None:
        module_logger.info(...)

Created: 23.12.2023
@author: Max Weise
"""

import logging
import typing


class Logger(typing.Protocol):
    """Define available logging functions."""

    def info(self, message: str):
        """Log a message with level info."""
        raise NotImplementedError()

    def warning(self, message: str):
        """Log a message with level warning."""
        raise NotImplementedError()

    def error(self, message: str):
        """Log a message with level error."""
        raise NotImplementedError()


class ConsoleLogger:
    """Log to std-out."""

    def __init__(
        self, logger_name: str, logging_level: int, format_string: str | None
    ) -> None:
        """Create a logger object that logs to std-out."""
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)
        # loggmessage_format = logging.Formatter()
        loggmessage_format = logging.Formatter(format_string)
        console_handler.setFormatter(loggmessage_format)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """Log a message with level info."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log a message with level warning."""
        self.logger.warning(message)

    def error(self, message: str):
        """Log a message with level error."""
        self.logger.error(message)


def logger_factory(
    logger_type: str,
    logger_name: str,
    logging_level: int,
    format_string: str | None = None,
) -> Logger:
    """Create a logger that can be used to print messages to the screen.

    Args:
        logger_type (str): The kind of logger that should be created.
        logger_name (str): The name of the logger displayed in the terminal.
        logging_level (int): The level used to filter logging messages.
        format_string (str | None): Specify the format by providing a string.
            Defaults to None.

    Returns:
        An object that implements the Logger interface.
    """
    available_loggers = {
        "console": ConsoleLogger,
    }
    logger = available_loggers[logger_type](
        logger_name, logging_level, format_string
    )
    return logger
