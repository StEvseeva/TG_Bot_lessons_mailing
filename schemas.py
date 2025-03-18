from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class SGroupAdd(BaseModel):
    name: str
    teacher_id: int
    description: Optional[str] = None

class SGroup(SGroupAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SGroupId(BaseModel):
    id: int

class STeacherAdd(BaseModel):
    name: str
    surname: Optional[str] = None
    chat_id: str

class STeacher(STeacherAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

