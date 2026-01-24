import os
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# -------------------------------------------------------------------
# Database config (via env vars, K8s-friendly)
# -------------------------------------------------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ehr")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# -------------------------------------------------------------------
# Models
# -------------------------------------------------------------------

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    records = relationship("ClinicalRecord", back_populates="patient")


class ClinicalRecord(Base):
    __tablename__ = "clinical_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="records")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    patient_id = Column(UUID(as_uuid=True), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# -------------------------------------------------------------------
# App init
# -------------------------------------------------------------------

app = FastAPI(title="Minimal EHR Backend")

@app.on_event("startup")
def startup():
    # Creates tables if they don't exist
    Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------------
# Utilities
# -------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# -------------------------------------------------------------------
# Health (for probes & recovery timing)
# -------------------------------------------------------------------

@app.get("/health")
def health():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="DB unavailable")

# -------------------------------------------------------------------
# Patients
# -------------------------------------------------------------------

@app.post("/patients")
def create_patient(name: str):
    db = get_db()
    patient = Patient(name=name)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@app.get("/patients/{patient_id}")
def get_patient(patient_id: uuid.UUID):
    db = get_db()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# -------------------------------------------------------------------
# Clinical Documentation
# -------------------------------------------------------------------

@app.post("/records")
def create_record(patient_id: uuid.UUID, content: str):
    db = get_db()

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    record = ClinicalRecord(
        patient_id=patient_id,
        content=content
    )

    audit = AuditLog(
        event_type="CREATE_RECORD",
        patient_id=patient_id
    )

    db.add(record)
    db.add(audit)
    db.commit()
    db.refresh(record)

    return record

@app.get("/records/{patient_id}")
def get_records(patient_id: uuid.UUID):
    db = get_db()
    records = (
        db.query(ClinicalRecord)
        .filter(ClinicalRecord.patient_id == patient_id)
        .all()
    )
    return records

# -------------------------------------------------------------------
# Break-the-Glass (Emergency Access)
# -------------------------------------------------------------------

@app.post("/break-glass")
def break_glass(patient_id: uuid.UUID):
    db = get_db()

    audit = AuditLog(
        event_type="BREAK_GLASS_ACCESS",
        patient_id=patient_id
    )

    db.add(audit)
    db.commit()

    return {
        "status": "emergency_access_logged",
        "patient_id": patient_id
    }
