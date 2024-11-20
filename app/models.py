# Models declared here represent a table in our database
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Post(Base):
    """Post database"""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publish = Column(Boolean, default=True)