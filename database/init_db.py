from database.connection import engine
from models.user import Base

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")