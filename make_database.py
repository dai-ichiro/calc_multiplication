from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer

engine = create_engine('sqlite:///try_again.db', echo = False)

Base = declarative_base()

class Multiplication(Base):

    __tablename__ = 'formula'

    id = Column('account_id', Integer, primary_key=True)
    q1 = Column('first_number', Integer)
    q2 = Column('second_number', Integer)

Base.metadata.create_all(bind=engine)