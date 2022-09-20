from app.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///" + os.path.join(BASE_DIR, "profile.db")

engine = create_engine(connection_string, echo=True)

Session = sessionmaker()

local_session = Session(bind=engine)

Base.metadata.create_all(engine)