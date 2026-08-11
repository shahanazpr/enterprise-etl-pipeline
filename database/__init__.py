from sqlalchemy.orm import declarative_base
from .connection import engine, SessionLocal

Base = declarative_base()