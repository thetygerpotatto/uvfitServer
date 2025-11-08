from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = (
    "mssql+pyodbc://CloudSA58d78e55:>hS6Kw#)G_c=tgk@datauvfit.database.windows.net:1433/"
    "uvfitdata?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
)

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
