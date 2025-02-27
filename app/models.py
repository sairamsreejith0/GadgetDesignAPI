from sqlalchemy import Column,String,Enum,DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base
class Gadget(Base):
    __tablename__ = "Gadgets"
    
    id = Column(UUID(as_uuid=True),primary_key = True,default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    status = Column(Enum("Available", "Deployed", "Destroyed", "Decommissioned", name="gadget_status"), default="Available")
    decommissioned_at = Column(DateTime, nullable=True)
    
class User(Base):
    __tablename__ = "Users"
    username = Column(String,primary_key = True)
    hashed_password = Column(String,nullable=False)