import sys
import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Importazione centralizzata dai modelli comuni
from models import Base, Patient, Encounter, ClinicalNote, AuditLog

# Configurazione (Aggiorna con IP Worker e Porta NodePort 30080)
DB_URL = "postgresql://postgres:secret@192.168.1.7:30432/ehr"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

class DBManager:
    def __init__(self):
        self.db = SessionLocal()

    def teardown(self):
        """Pulisce completamente il database (Reset Baseline)"""
        print("[!] Esecuzione Teardown: svuotamento tabelle...")
        try:
            # TRUNCATE è molto più veloce di DELETE per grandi volumi
            self.db.execute(text("TRUNCATE patients, encounters, clinical_notes, audit_log RESTART IDENTITY CASCADE;"))
            self.db.commit()
            print("[OK] Database riportato allo stato zero.")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Teardown fallito: {e}")

    def seed(self, num_patients=500):
        """Popolamento massivo per Baseline Operativa"""
        print("sium")
        print(f"[*] Seeding di {num_patients} pazienti...")
        try:
            for i in range(num_patients):
                p = Patient(name=f"Test_Patient_{i}", tax_code=f"TAX-{uuid.uuid4().hex[:8]}")
                self.db.add(p)
                self.db.flush()

                for _ in range(3): # 3 visite per paziente
                    e = Encounter(patient_id=p.id, encounter_type="ROUTINE")
                    self.db.add(e)
                    self.db.flush()

                    for _ in range(10): # 10 note per visita
                        n = ClinicalNote(
                            encounter_id=e.id, 
                            patient_id=p.id,
                            note_type="PROGRESS",
                            content="Dato clinico per test recovery " * 20,
                            created_at=datetime.utcnow() - timedelta(hours=random.randint(0, 720))
                        )
                        self.db.add(n)
                
                if i % 100 == 0:
                    self.db.commit()
                    print(f"[+] Processati {i} pazienti...")
            self.db.commit()
            print(f"[OK] Inseriti circa {num_patients * 3 * 10} record clinici.")
            print("[OK] Dataset Baseline creato con successo.")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Seed fallito: {e}")

    def corrupt(self, hours=24):
        """Iniezione guasto (Fault Injection)"""
        print(f"[*] Corruzione dati: eliminazione ultime {hours} ore...")
        limit = datetime.utcnow() - timedelta(hours=hours)
        res = self.db.execute(text("DELETE FROM clinical_notes WHERE created_at > :lim"), {"lim": limit})
        self.db.commit()
        print(f"[OK] Eliminati {res.rowcount} record clinici.")

    def stats(self):
        """Verifica Baseline funzionale"""
        p = self.db.query(Patient).count()
        e = self.db.query(Encounter).count()
        n = self.db.query(ClinicalNote).count()
        size_query = text("SELECT pg_size_pretty(pg_database_size(current_database()))")
        db_size = self.db.execute(size_query).scalar()
        print(f"--- Stats DB --- \nPazienti: {p} \nVisite: {e} \nNote: {n} \nDimensione DB: {db_size}")

if __name__ == "__main__":
    mgr = DBManager()
    
    if len(sys.argv) < 2:
        print("Uso: python db_manager.py [teardown | seed | corrupt | stats]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "teardown":
        mgr.teardown()
    elif cmd == "seed":
        mgr.seed(10000)
    elif cmd == "corrupt":
        mgr.corrupt(48)
    elif cmd == "stats":
        mgr.stats()