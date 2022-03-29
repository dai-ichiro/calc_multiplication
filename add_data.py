from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from make_database import Multiplication

engine = create_engine('sqlite:///try_again.db')

session = sessionmaker(bind=engine)()

session.add(
    Multiplication(
        q1 = 99,
        q2 = 99
    )
)

session.commit()
session.close()