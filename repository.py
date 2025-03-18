from db import new_session, Group, Teacher
from schemas import SGroup, SGroupAdd, STeacherAdd
from sqlalchemy import select

class GroupRepository:
    @classmethod
    async def put(cls, data: SGroupAdd) -> int:
        async with new_session() as session:
            group_dict = data.model_dump()

            group = Group(**group_dict)
            session.add(group)
            await session.flush()
            await session.commit()
            return group.id

    @classmethod
    async def get(cls, id: int = None) -> list[SGroup]:
        async with new_session() as session:
            query = select(Group)
            if id:
                query = query.where(Group.id == id)
            result = await session.execute(query)
            group_models = result.scalars().all()
            group_models = [SGroup.model_validate(model) for model in group_models]
            return group_models
        

class TeacherRepository:
    @classmethod
    async def put(cls, data: STeacherAdd) -> int:
        async with new_session() as session:
            teacher_dict = data.model_dump()
            print()
            teacher = Teacher(**teacher_dict)
            session.add(teacher)
            await session.flush()
            await session.commit()
            return teacher.id
