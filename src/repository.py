from db import new_session, Group, User
from schemas import SGroupGet, SGroupBase, SUserBase, SUserBase
from sqlalchemy import select

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
            query = select(Group)
            if id:
                query = query.where(Group.id == id)
            result = await session.execute(query)
            group_models = result.scalars().all()
            group_models = [SGroupGet.model_validate(model) for model in group_models]
            logger_db.info(f'get objects User | {len(group_models)} items found')
            return group_models
        

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
            logger_db.info(f'add object User | teacher: \'{data.is_teacher}\' name: \'{data.name}\' surname: \'{data.surname}\' id: \'{user.chat_id}\'')
            return True

    @classmethod
    async def get(cls, chat_id: int = None) -> list[SUserBase]:
        async with new_session() as session:
            query = select(User)
            if id:
                query = query.where(User.chat_id == chat_id)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_models = [SUserBase.model_validate(model) for model in user_models]
            logger_db.info(f'get objects User | {len(user_models)} items found')
            return user_models
      
