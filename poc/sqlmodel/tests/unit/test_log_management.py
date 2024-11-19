import logging
import pytest

from src.tools.log_management import LogManagement


@pytest.mark.parametrize("verbosity,logger_name", [(None, "test"), (None, "")])
def test_init(verbosity, logger_name) -> None:
    log_ref = LogManagement(verbosity, logger_name)
    assert log_ref is not None


@pytest.mark.parametrize("verbosity", [None, 0, 1, 2, 3])
def test_get_logger(verbosity) -> None:
    log_ref = LogManagement(verbosity, "")
    logger = log_ref.get_logger()
    assert logger is not None


@pytest.mark.parametrize(
    "verbosity,expected_level",
    [
        (None, logging.CRITICAL),
        (0, logging.CRITICAL),
        (1, logging.WARNING),
        (2, logging.INFO),
        (3, logging.DEBUG),
    ],
)
def test_get_logging_level(verbosity, expected_level) -> None:
    log_ref = LogManagement(verbosity, "")
    current_level = log_ref.get_logging_level()
    assert current_level == expected_level
