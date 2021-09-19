from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_CONNECTION_STRING = 'sqlite:///hw906.db'

engine = create_engine(_CONNECTION_STRING, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()
# metadata = Base.metadata


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    address = Column(String)
    email = Column(String)
    tags = Column(String)

    phones = relationship("Phone", back_populates='record',
                          cascade="all, delete, delete-orphan")

    def __repr__(self):
        result = ""
        result += f'|{self.id if self.id else " ":<5}| {self.name if self.name else " ":<25}| { self.phones[0].phone_value if self.phones else " ":<15} | {str(self.birthday) if self.birthday else " ":<11}|{self.address if self.address else " ":<30}|  {self.email if self.email else " ":<30}| {self.tags if self.tags else " ":<15}|\n'
        if len(self.phones) > 1:
            for elem in self.phones[1:]:
                result += f'|     |                          | {elem.phone_value: <15} |            |                              |                                |                | \n'
        result += f"{145*'_'}\n"
        return result


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    phone_value = Column(String, nullable=False)
    record_id = Column(Integer, ForeignKey('records.id'))

    record = relationship("Record", back_populates="phones")

    def __repr__(self):
        return "<Phone(phone_value='%s')>" % self.phone_value


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note_tags = Column(String)
    note_text = Column(String)


metadata = Base.metadata
metadata.bind = engine
metadata.create_all(engine)
