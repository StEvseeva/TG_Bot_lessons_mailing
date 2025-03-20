from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class SGroupBase(BaseModel):
    name: str
    teacher_id: int
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SUserBase(BaseModel): # TODO check models and actual attrs
    chat_id: int
    name: str
    surname: str
    is_teacher: Optional[bool] = False
    groups: Optional[List[SGroupBase]] = []
    teacher_groups: Optional[List[SGroupBase]] = []

    model_config = ConfigDict(from_attributes=True)

class SGroupGet(SGroupBase):
    id: int
    students: Optional[List[SUserBase]] = []

