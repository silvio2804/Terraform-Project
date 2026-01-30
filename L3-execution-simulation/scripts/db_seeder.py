import os
import sys
import uuid
import random
from datetime import datetime, timedelta

from models import Base, Patient, Encounter, ClinicalNote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurazione DB (Usa l'IP del Worker e la NodePort 30080)
DB_URL = "postgresql://postgres:secret@192.168.1.7:30432/ehr"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

def run_seeder(num_patients=500):
    print(f"[*] Inizio seeding su {DB_URL}")
    try:
        for i in range(num_patients):
            # Creazione Paziente
            new_p = Patient(
                name=f"Patient_{uuid.uuid4().hex[:6]}",
                tax_code=f"TAX-{i}-{uuid.uuid4().hex[:4]}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
            )
            session.add(new_p)
            session.flush()

            # Creazione Encounter (Visite)
            for _ in range(random.randint(2, 4)):
                new_e = Encounter(
                    patient_id=new_p.id,
                    encounter_type=random.choice(["ROUTINE", "EMERGENCY"]),
                    admitted_at=new_p.created_at + timedelta(days=1)
                )
                session.add(new_e)
                session.flush()

                # Creazione ClinicalNote (Note cliniche pesanti)
                for _ in range(random.randint(10, 15)):
                    new_n = ClinicalNote(
                        encounter_id=new_e.id,
                        patient_id=new_p.id,
                        note_type="PROGRESS_NOTE",
                        content="Dato clinico strutturato per test di recovery. " * 30,
                        created_at=new_e.admitted_at + timedelta(hours=random.randint(1, 12))
                    )
                    session.add(new_n)
            
            if i % 50 == 0:
                session.commit()
                print(f"[+] Processati {i} pazienti...")

        session.commit()
        print("[OK] Dataset Baseline creato con successo.")
    except Exception as e:
        session.rollback()
        print(f"[ERRORE] Seeding interrotto: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    run_seeder(500)