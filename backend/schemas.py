from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttendanceCreate(BaseModel):
    studentid: int
    courseid: int
    datetime: Optional[datetime] = None