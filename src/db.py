from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from typing import Optional, List, Text

engine = create_async_engine(
    "sqlite+aiosqlite:///litedb.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

associate_students_groups = Table(
    "students_groups",
    Model.metadata,
    Column("student_chat_id", ForeignKey("users.chat_id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

class Group(Model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    teacher_chat_id: Mapped[int] = mapped_column(ForeignKey("users.chat_id"))
    posts: Mapped[Optional[List["Post"]]] = relationship(lazy='selectin')
    students: Mapped[Optional[List["User"]]] = relationship(
        secondary=associate_students_groups, back_populates="groups")

class User(Model):
    __tablename__ = "users"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    is_teacher: Mapped[Optional[bool]] = mapped_column(default=False)
    name: Mapped[str]
    surname: Mapped[Optional[str]]
    username: Mapped[str]
    teacher_posts: Mapped[Optional[List['Post']]] = relationship(lazy='selectin')
    teacher_groups: Mapped[Optional[List[Group]]] = relationship(lazy='selectin')
    groups: Mapped[Optional[List[Group]]] = relationship(
        lazy='selectin', secondary=associate_students_groups, 
        back_populates="students")

class Post(Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    teacher_chat_id: Mapped[int] = mapped_column(ForeignKey("users.chat_id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    content: Mapped[Text]
    sheduler_job_id: Mapped[int]

async def create_posts():
    async with engine.begin() as conn:
        await conn.run_sync(Post.metadata.create_all)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    
async def delete_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)