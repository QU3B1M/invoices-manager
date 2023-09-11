from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.core.utils import get_random_string


class Invoice(BaseModel):
    id: str = Field(default_factory=get_random_string, max_length=16)
    date: datetime = Field(default_factory=datetime.now)
    due_date: datetime = Field(default_factory=datetime.now)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., max_length=3)
    description: str = Field(..., max_length=100)
