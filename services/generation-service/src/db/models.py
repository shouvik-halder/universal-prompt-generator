from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Platform(Base):
    __tablename__ = "platforms"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # text, image, audio, video
    enabled = Column(Boolean, default=True)
    config = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    templates = relationship("Template", back_populates="platform")


class Intent(Base):
    __tablename__ = "intents"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    enabled = Column(Boolean, default=True)
    config = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    templates = relationship("Template", back_populates="intent")


class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform_id = Column(String(50), ForeignKey("platforms.id"), nullable=False)
    intent_id = Column(String(50), ForeignKey("intents.id"), nullable=False)
    variant = Column(String(100), default="default")
    version = Column(Integer, default=1)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text, nullable=False)
    variables = Column(JSONB, default=[])
    settings = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    platform = relationship("Platform", back_populates="templates")
    intent = relationship("Intent", back_populates="templates")