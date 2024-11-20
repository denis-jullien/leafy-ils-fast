import logging


class LogManagement:
    """
    A class used to manage verbosity
    """

    def __init__(self, verbosity: int | None, logger_name: str) -> None:
        """
        Inititalize the verbosity

        Parameters
        ----------
        verbosity: integer
            verbosity level

        logger_name: str

        Returns
        -------
        None
        """
        # Define application logging
        if verbosity is None or verbosity == 0:
            self._logging_level = logging.CRITICAL
        elif verbosity == 1:
            self._logging_level = logging.WARNING
        elif verbosity == 2:
            self._logging_level = logging.INFO
        else:
            self._logging_level = logging.DEBUG

        self._logger = logging.getLogger(logger_name)
        logging.basicConfig(level=self._logging_level)

        self._log_formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d > [%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
        )

        # Start logging handler
        self._log_handler = logging.StreamHandler()
        self._log_handler.setFormatter(self._log_formatter)
        self._log_handler.setLevel(self._logging_level)

        self._logger.propagate = False
        self._logger.addHandler(self._log_handler)

    def get_logger(self):
        """
        Get logger reference

        Returns
        -------
        logger reference from logging library
        """
        return self._logger

    def get_logging_level(self):
        """
        Get logging level

        Returns
        -------
        logging level value from logging library
        """
        return self._logging_level
