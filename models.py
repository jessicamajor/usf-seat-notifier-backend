from typing import Optional
from sqlmodel import SQLModel, Field

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str
    crn: str
    last_seats: int = 0
