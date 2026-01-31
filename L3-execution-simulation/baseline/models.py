import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    tax_code = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
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