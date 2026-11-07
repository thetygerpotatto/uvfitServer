from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import os

# Set DATABASE_URL in the environment (Azure App Service > Configuration),
# never hardcode credentials in the repo.
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

class BaseTable:
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

Base = declarative_base(cls=BaseTable)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
