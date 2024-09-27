from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import settings

engine = create_engine(url=settings.DATABASE_URL_psycopg)
session_maker = sessionmaker(engine)
