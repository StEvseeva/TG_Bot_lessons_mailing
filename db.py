from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from typing import Optional, List

engine = create_async_engine(
    "sqlite+aiosqlite:///litedb.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

associate_students_groups = Table(
    "students_groups",
    Model.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)



class Group(Model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    students: Mapped[Optional[List["Student"]]] = relationship(secondary=associate_students_groups, back_populates="groups")


class Teacher(Model):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    name: Mapped[str]
    surname: Mapped[Optional[str]]
    groups: Mapped[Optional[List[Group]]] = relationship()


class Student(Model):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    name: Mapped[str]
    surname: Mapped[str]
    groups: Mapped[Optional[List[Group]]] = relationship(secondary=associate_students_groups, back_populates="students")



async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    
async def delete_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)