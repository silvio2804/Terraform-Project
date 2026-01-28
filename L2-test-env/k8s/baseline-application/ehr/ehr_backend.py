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
    ForeignKey,
    text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# -------------------------------------------------------------------
# Database config
# -------------------------------------------------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ehr")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
    tax_code = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relazione verso Encounter
    encounters = relationship("Encounter", back_populates="patient", cascade="all, delete-orphan")

class Encounter(Base):
    __tablename__ = "encounters"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    encounter_type = Column(String, nullable=False)
    admitted_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="encounters")
    notes = relationship("ClinicalNote", back_populates="encounter", cascade="all, delete-orphan")

class ClinicalNote(Base):
    __tablename__ = "clinical_notes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    note_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    encounter = relationship("Encounter", back_populates="notes")

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    patient_id = Column(UUID(as_uuid=True), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# -------------------------------------------------------------------
# App init & Utilities
# -------------------------------------------------------------------

app = FastAPI(title="EHR Backend - Recovery Scenario S1")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# -------------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------------

@app.get("/health")
def health():
    try:
        db = get_db()
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="DB unavailable")

@app.post("/patients")
def create_patient(name: str, tax_code: str):
    db = get_db()
    patient = Patient(name=name, tax_code=tax_code)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@app.post("/seed-data")
def seed_data(num_patients: int = 100):
    db = get_db()
    try:
        for i in range(num_patients):
            p = Patient(name=f"Patient {uuid.uuid4().hex[:8]}", tax_code=f"TX-{uuid.uuid4().hex[:10]}")
            db.add(p)
            db.flush() 
            
            for _ in range(4):
                e = Encounter(patient_id=p.id, encounter_type="ROUTINE")
                db.add(e)
                db.flush()
                
                for _ in range(10):
                    n = ClinicalNote(
                        encounter_id=e.id, 
                        patient_id=p.id, 
                        note_type="PROGRESS_NOTE", 
                        content="Dato clinico rilevante per test recovery..." * 50
                    )
                    db.add(n)
        db.commit()
        return {"message": f"Seeding completato per {num_patients} pazienti"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_database_stats():
    db = get_db()
    return {
        "patients": db.query(Patient).count(),
        "encounters": db.query(Encounter).count(),
        "clinical_notes": db.query(ClinicalNote).count()
    }

@app.delete("/teardown/all")
def hard_reset_database():
    db = get_db()
    try:
        # Pulizia radicale per reset esperimento
        db.execute(text("TRUNCATE patients, encounters, clinical_notes, audit_log RESTART IDENTITY CASCADE;"))
        db.commit()
        return {"status": "success", "message": "DB pulito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))