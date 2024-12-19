from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String)  # Full-Time, Part-Time, etc.
    description = Column(String)
    location = Column(String)
    salary = Column(String)  # Changed to String to handle ranges like "$70K - $80K"
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="jobs") 