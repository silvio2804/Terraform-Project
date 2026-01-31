import sys
import random
import uuid
from datetime import datetime, timedelta
import concurrent.futures
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Importazione centralizzata dai modelli comuni
from models import Base, Patient, Encounter, ClinicalNote, AuditLog

# Configurazione (Aggiorna con IP Worker e Porta NodePort 30080)
DB_URL = "postgresql://postgres:secret@192.168.1.7:30432/ehr"

engine = create_engine(
    DB_URL, 
    pool_size=20,       # Numero di connessioni mantenute aperte
    max_overflow=10     # Connessioni extra in caso di picco
)
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

    def seed_worker(self, num_patients_chunk):
        """Funzione eseguita dal singolo thread per inserire un blocco di pazienti"""
        db = SessionLocal()
        try:
            for i in range(num_patients_chunk):
                p = Patient(name=f"Threaded_P_{uuid.uuid4().hex[:6]}", tax_code=f"TX-{uuid.uuid4().hex[:10]}")
                db.add(p)
                db.flush()

                for _ in range(3):
                    e = Encounter(patient_id=p.id, encounter_type="EMERGENCY")
                    db.add(e)
                    db.flush()

                    for _ in range(10):
                        n = ClinicalNote(
                            encounter_id=e.id, 
                            patient_id=p.id,
                            note_type="PROGRESS",
                            content="Dato clinico massivo per stress test RAM..." * 30,
                            created_at=datetime.utcnow() - timedelta(hours=random.randint(0, 100))
                        )
                        db.add(n)
                
                if i % 10 == 0: # Commit frequenti per tenere alta la pressione sui log
                    db.commit()
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Errore worker: {e}")
        finally:
            db.close()

    def seed_parallel(self, total_patients=100000, num_threads=5):
        """Gestisce la distribuzione del carico tra i thread"""
        print(f"[*] Avvio seeding parallelo: {total_patients} pazienti su {num_threads} thread...")
        chunk_size = total_patients // num_threads

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Distribuisce il lavoro ai thread
            futures = [executor.submit(self.seed_worker, chunk_size) for _ in range(num_threads)]
            
            # Attende il completamento
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread ha generato un errore: {e}")
        
        print("[OK] Seeding parallelo completato.")

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
        mgr.seed_parallel(100000,8)
    elif cmd == "corrupt":
        mgr.corrupt(48)
    elif cmd == "stats":
        mgr.stats()