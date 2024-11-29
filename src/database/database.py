from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_db():
   Base.metadata.create_all(bind=engine)


# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telegram_id = Column(String, unique=True)
    role = Column(String)  # 'student' or 'teacher'
    status = Column(Boolean, default=True)



# # Модель курса
# class Course(Base):
#     __tablename__ = "courses"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(Text)
#     teacher_id = Column(Integer, ForeignKey('users.id'))
#
#
# # Модель задания
# class Assignment(Base):
#     __tablename__ = "assignments"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     description = Column(Text)
#     course_id = Column(Integer, ForeignKey('courses.id'))
#     due_date = Column(DateTime)
#     group_id = Column(Integer, ForeignKey('groups.id'))
#
#
# # Модель выполненного задания
# class Submission(Base):
#     __tablename__ = "submissions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     assignment_id = Column(Integer, ForeignKey('assignments.id'))
#     student_id = Column(Integer, ForeignKey('users.id'))
#     file = Column(String)  # Путь к файлу
#     submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
#     checked = Column(Boolean, default=False)
#     grade = Column(Integer)
#     feedback = Column(Text)


Base.metadata.create_all(bind=engine)
