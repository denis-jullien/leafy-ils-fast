# Typing

from typing import Any, TypeVar, Union

from sqlmodel.sql.base import Executable
from sqlmodel.sql.expression import Select, SelectOfScalar

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
