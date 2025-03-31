from db import new_session, Group, User
from schemas import SGroupGet, SGroupBase, SUserBase, SUserBase, SPost
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import List

from loggers import get_logger

logger_db = get_logger(__name__)
class GroupRepository:
    @classmethod
    async def put(cls, data: SGroupBase) -> int:
        async with new_session() as session:
            group_dict = data.model_dump()
            group = Group(**group_dict)
            session.add(group)
            await session.flush()
            await session.commit()
            return group.id

    @classmethod
    async def get(cls, id: int = None) -> list[SGroupGet]:
        async with new_session() as session:
            query = select(Group).options(selectinload(Group.students))
            if id:
                query = query.where(Group.id == id)
            result = await session.execute(query)
            group_models = result.scalars().all()
            group_models = [SGroupGet.model_validate(model) for model in group_models]
            logger_db.debug(f'get objects Group | {len(group_models)} items found')
            return group_models

    @classmethod
    async def get_by_teacher_id(cls, teacher_chat_id: int = None) -> list[SGroupGet]:
        async with new_session() as session:
            query = select(Group).where(Group.teacher_chat_id == teacher_chat_id)
            query = query.options(selectinload(Group.students))
            result = await session.execute(query)
            group_models = result.scalars().all()
            group_models = [SGroupGet.model_validate(model) for model in group_models]
            logger_db.debug(f'get objects User | {len(group_models)} items found')
            return group_models
    
    @classmethod
    async def delete(cls, id: int = None) -> bool:
        async with new_session() as session:
            group = await session.get(Group, id)
            session.delete(group)
            await session.commit
            return True

class UserRepository:
    @classmethod
    async def put(cls, data: SUserBase) -> bool:
        async with new_session() as session:
            user_dict = data.model_dump()
            print()
            user = User(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            logger_db.info(f'add object User | teacher: \'{data.is_teacher}\' name: \'{data.name}\' surname: \'{data.surname}\' username: \'{user.username}\'')
            return True

    @classmethod
    async def get(cls, chat_ids: List[int] = None, only_students: bool = False) -> list[SUserBase]:
        async with new_session() as session:
            query = select(User)
            if chat_ids:
                query = query.filter(User.chat_id.in_(chat_ids))
            if only_students:
                query = query.where(User.is_teacher == True)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_models = [SUserBase.model_validate(model) for model in user_models]
            logger_db.info(f'get objects User | {len(user_models)} items found')
            return user_models
        
    @classmethod
    async def add_to_group(cls, student_chat_id: int, group_id: SGroupGet) -> bool:
        async with new_session() as session:
            student = await session.get(User, student_chat_id)
            group = await session.get(Group, group_id)
            if not student:
                logger_db.info(f'add group to Student | student with id {student_chat_id} not found')
                return False

            student.groups.append(group)
            await session.commit()
            logger_db.info(f'add group to Student | group: {group.name} student: {student.surname} {student.name}')
            return True
      
class PostRepository:
    @classmethod
    async def put(cls, data: SPost) -> bool:
        pass