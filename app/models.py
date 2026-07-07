from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from datetime import datetime
from app.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String, primary_key=True)  # session_id (UUID from client)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatTurn(Base):
    __tablename__ = "chat_turns"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    query = Column(Text)
    answer = Column(Text)
    confidence = Column(Float)
    escalated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class UnresolvedQuery(Base):
    __tablename__ = "unresolved_queries"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    query = Column(Text)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)