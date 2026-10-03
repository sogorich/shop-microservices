from typing import TypeVar
from sqlmodel import SQLModel


ModelT = TypeVar("ModelT", bound=SQLModel)