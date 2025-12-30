from sqlalchemy import Column, Integer, String
from .database import Base

class Creator(Base):
    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    life_years = Column(String)
    country = Column(String)
    main_style = Column(String)
