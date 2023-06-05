from pydantic import BaseModel, Field
from random import choice
from typing import Union


class Task(BaseModel):
    title: str = Field(max_length=32)
    description: Union[str, None] = Field(max_length=200)
    status: bool = Field(default=False)


tasks = []

# filling test data
for i in range(10):
    tasks.append(Task(title=f"title{i}",
                      description=f"description{i}",
                      status=choice([True, False])))
