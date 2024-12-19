from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CompanyResponse(BaseModel):
    """
    Schema for embedding company details in job responses.
    """
    name: str
    description: str
    contact_email: EmailStr
    contact_phone: str


class JobBase(BaseModel):
    title: str
    type: str
    description: str
    location: str
    salary: str


class JobCreate(JobBase):
    """
    Schema for creating a new job.
    """
    company_name: str
    company_description: str
    company_contact_email: EmailStr
    company_contact_phone: str


class JobUpdate(BaseModel):
    """
    Schema for updating an existing job.
    """
    title: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    company_contact_email: Optional[EmailStr] = None
    company_contact_phone: Optional[str] = None


class JobResponse(JobBase):
    """
    Schema for serializing job responses.
    """
    id: int
    created_at: datetime
    company: CompanyResponse

    class Config:
        from_attributes = True
