# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    description: Optional[str] = Field(
        'no description',
        title='Task description',
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title='Shows whether the task was completed',
    )

    user: str = Field(
        'no uuid',
        title='User UUID',
        max_length=1024,
    )

    class Config:
        schema_extra = {
            'example': {
                'description': 'Buy baby diapers',
                'completed': False,
                'user': 'valid uuid'
            }
        }


class User(BaseModel):
    name: str = Field(
        'no name',
        title='User name',
        max_length=1024,
    )

    class Config:
        schema_extra = {
            'example': {
                'name': 'Rogerio Batista',
            }
        }
