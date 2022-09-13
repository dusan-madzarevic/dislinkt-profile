from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    ime = Column(String)
    prezime = Column(String)
    telefon = Column(String)
    datumRodjenja = Column(Date)
    pol = Column(String)
    role = Column(String(25), nullable=False)
    # posts = relationship("Post", back_populates="author")
    # reactions = relationship("Reaction", back_populates="author")

