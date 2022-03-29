from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from make_database import Multiplication

engine = create_engine('sqlite:///try_again.db')

session = sessionmaker(bind=engine)()

query_result = session.query(Multiplication)
for formula in query_result:
    print('%d X %d'%(formula.q1, formula.q2))
session.close()

input()