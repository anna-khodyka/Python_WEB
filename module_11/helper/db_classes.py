from flask.globals import current_app
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# _CONNECTION_STRING = "sqlite:///hw907.db"
_CONNECTION_STRING = os.getenv('MY_DB_NAME')
# _CONNECTION_STRING = "sqlite:///test.db"

engine = create_engine(_CONNECTION_STRING, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    address = Column(String)
    email = Column(String)
    tags = Column(String)

    phones = relationship(
        "Phone", back_populates="record", cascade="all, delete, delete-orphan"
    )


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    phone_value = Column(String, nullable=False)
    record_id = Column(Integer, ForeignKey("records.id"))

    record = relationship("Record", back_populates="phones")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    note_tags = Column(String)
    note_text = Column(String)
    created_at = Column(Date)


Base.metadata.bind = engine
Base.metadata.create_all(engine)
