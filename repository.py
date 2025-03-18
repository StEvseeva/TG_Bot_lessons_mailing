from db import new_session, Group, Teacher, Student
from schemas import SGroup, SGroupAdd, STeacherAdd, STeacher, SStudentAdd, SStudent
from sqlalchemy import select

from loggers import get_logger

logger_db = get_logger(__name__)
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
            logger_db.info(f'add object Teacher | name: {data.name} surname: {data.surname}')
            teacher_dict = data.model_dump()
            print()
            teacher = Teacher(**teacher_dict)
            session.add(teacher)
            await session.flush()
            await session.commit()
            return teacher.id

    @classmethod
    async def get(cls, chat_id: int = None) -> list[STeacher]:
        async with new_session() as session:
            logger_db.info(f'get object Teacher | chat_id: {chat_id}')
            query = select(Teacher)
            if id:
                query = query.where(Teacher.chat_id == chat_id)
            result = await session.execute(query)
            teacher_models = result.scalars().all()
            teacher_models = [STeacher.model_validate(model) for model in teacher_models]
            return teacher_models
       
class StudentRepository:
    @classmethod
    async def put(cls, data: SStudentAdd) -> int:
        async with new_session() as session:
            logger_db.info(f'add object Student | name: {data.name} surname: {data.surname}')
            student_dict = data.model_dump()
            print()
            student = Student(**student_dict)
            session.add(student)
            await session.flush()
            await session.commit()
            return student.id
    
    @classmethod
    async def get(cls, chat_id: int = None) -> list[SStudent]:
        async with new_session() as session:
            logger_db.info(f'get object Student | chat_id: {chat_id}')
            query = select(Student)
            if id:
                query = query.where(Student.chat_id == chat_id)
            result = await session.execute(query)
            student_models = result.scalars().all()
            student_models = [SStudent.model_validate(model) for model in student_models]
            return student_models