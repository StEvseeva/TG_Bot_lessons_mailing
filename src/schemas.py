from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Text

class SPost(BaseModel):
    name: str
    teacher_chat_id: int
    group_id: int
    content: Text
    sheduler_job_id: int

class SGroupBase(BaseModel):
    name: str
    teacher_chat_id: int
    description: Optional[str] = None
    posts: Optional[List[SPost]] = []

    model_config = ConfigDict(from_attributes=True)

class SUserCreds(BaseModel):
    chat_id: int
    name: str
    surname: str
    username: str

    model_config = ConfigDict(from_attributes=True)
    
class SUserBase(BaseModel): # TODO check models and actual attrs
    chat_id: int
    name: str
    surname: str
    username: str
    is_teacher: Optional[bool] = False
    groups: Optional[List[SGroupBase]] = []
    teacher_groups: Optional[List[SGroupBase]] = []
    teacher_posts: Optional[List[SPost]] = []

    model_config = ConfigDict(from_attributes=True)

class SGroupGet(SGroupBase):
    id: int
    students: Optional[List[SUserCreds]] = []

class SGroupUpd(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    students: Optional[List[int]] = []

