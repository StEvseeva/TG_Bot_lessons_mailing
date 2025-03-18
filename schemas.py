from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class SGroupAdd(BaseModel):
    name: str
    teacher_id: int
    description: Optional[str] = None

class SGroup(SGroupAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SPublicProfile(BaseModel):
    name: str
    surname: str

class STeacherAdd(SPublicProfile):
    chat_id: int

class STeacher(STeacherAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SStudentAdd(SPublicProfile):
    chat_id: int

class SStudent(SStudentAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
