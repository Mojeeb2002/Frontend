from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Job, Company
from app.schemas import JobCreate, JobUpdate, JobResponse
from typing import List

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    """
    Retrieve a list of all jobs with embedded company details.
    """
    jobs = db.query(Job).options(joinedload(Job.company)).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific job by ID with embedded company details.
    """
    job = db.query(Job).options(joinedload(Job.company)).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job and associate it with a company.
    """
    # Create the company
    db_company = Company(
        name=job.company_name,
        description=job.company_description,
        contact_email=job.company_contact_email,
        contact_phone=job.company_contact_phone,
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    # Create the job
    db_job = Job(
        title=job.title,
        type=job.type,
        description=job.description,
        location=job.location,
        salary=job.salary,
        company_id=db_company.id,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    """
    Update an existing job by ID. Updates both job and associated company details.
    """
    db_job = db.query(Job).options(joinedload(Job.company)).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update job fields
    job_data = job.dict(exclude_unset=True)
    for key, value in job_data.items():
        if hasattr(db_job, key):
            setattr(db_job, key, value)

    # Update company fields if provided
    if "company_name" in job_data or "company_description" in job_data:
        company_data = {
            "name": job_data.get("company_name", db_job.company.name),
            "description": job_data.get("company_description", db_job.company.description),
            "contact_email": job_data.get("company_contact_email", db_job.company.contact_email),
            "contact_phone": job_data.get("company_contact_phone", db_job.company.contact_phone),
        }
        for key, value in company_data.items():
            setattr(db_job.company, key, value)

    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job by ID.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}
