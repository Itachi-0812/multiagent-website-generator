from pydantic import BaseModel
from typing import List, Optional


class Task(BaseModel):
    id: str
    agent: str
    task: str
    depends_on: List[str] = []


class Plan(BaseModel):
    website_type: str
    pages: list[str]
    components: list[str]
    tasks: list[Task]
    user_prompt: str