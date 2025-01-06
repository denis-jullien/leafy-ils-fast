from datetime import date
from typing import Any, TypeVar, Union

from sqlmodel.sql.base import Executable
from sqlmodel.sql.expression import Select, SelectOfScalar

# Typing

_TSelectParam = TypeVar("_TSelectParam", bound=Any)

STATEMENT_TYPE = Union[
    Select[_TSelectParam],
    SelectOfScalar[_TSelectParam],
    Executable[_TSelectParam],
]

# Constants for Pagination

DEFAULT_MINIMAL_VALUE = 1

LIMIT_DEFAULT_VALUE = 20
LIMIT_MAXIMAL_VALUE = 100

DATE_DEFAULT_START_VALUE = "2016-09-01"
DATE_DEFAULT_END_VALUE = f"{date.today()}"
