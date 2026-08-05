from pydantic import BaseModel
from typing import List


class WebsitePlan(BaseModel):
    website_type: str
    sections: List[str]