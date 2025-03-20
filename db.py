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
    Column("student_id", ForeignKey("users.chat_id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

class Group(Model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.chat_id"))
    students: Mapped[Optional[List["User"]]] = relationship(secondary=associate_students_groups, back_populates="groups")


class User(Model):
    __tablename__ = "users"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    is_teacher: Mapped[Optional[bool]] = mapped_column(default=False)
    name: Mapped[str]
    surname: Mapped[Optional[str]]
    teacher_groups: Mapped[Optional[List[Group]]] = relationship(lazy='selectin')
    groups: Mapped[Optional[List[Group]]] = relationship(lazy='selectin', secondary=associate_students_groups, back_populates="students")


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    
async def delete_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)