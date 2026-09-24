from database import engine, Base
from app import app

Base.metadata.create_all(bind=engine)