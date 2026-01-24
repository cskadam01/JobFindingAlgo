from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database.config import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(50), nullable=True)
    title = Column(String(255), nullable=False)
    link = Column(Text, nullable=False, unique=True)

    place = Column(String(255), nullable=True)
    wage = Column(String(255), nullable=True)
    desc = Column(Text, nullable=True)

    ai_score = Column(Float, nullable=True)
    ai_feedback = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    label = Column(Integer, nullable=False)  # 1 = érdekel, 0 = nem

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job")