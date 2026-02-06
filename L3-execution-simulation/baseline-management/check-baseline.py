import requests
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configurazione target
API_URL = "http://192.168.1.7:30080"
EXPECTED_THRESHOLDS = {
    "patients": 100,        
    "encounters": 400,      
    "clinical_notes": 1000  
}

DB_URL = "postgresql://postgres:secret@192.168.1.7:30032/ehr"

engine = create_engine(
    DB_URL, 
    pool_size=20,       
    max_overflow=10     
)
SessionLocal = sessionmaker(bind=engine)

def check_service_availability():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        if r.status_code == 200:
            print("[OK] Service Availability: Backend UP & DB Connected")
            return True
        print(f"[FAIL] Service returned {r.status_code}")
        return False
    except Exception as e:
        print(f"[FAIL] Connection Error: {e}")
        return False

def check_data_volume():
    try:
        r = requests.get(f"{API_URL}/stats", timeout=5)
        data = r.json()
        
        is_valid = True
        for entity, min_count in EXPECTED_THRESHOLDS.items():
            actual = data.get(entity, 0)
            if actual < min_count:
                print(f"[FAIL] Volume {entity}: Found {actual}, Expected >{min_count}")
                is_valid = False
            else:
                print(f"[OK] Volume {entity}: {actual} records (Threshold met)")
        
        return is_valid
    except Exception as e:
        print(f"[FAIL] Stats Check Error: {e}")
        return False

def get_db_size():
    """Cattura la dimensione del DB in formato leggibile e byte raw"""
    db = SessionLocal()
    try:
        query = text("""
            SELECT 
                pg_size_pretty(pg_database_size(current_database())) as formatted,
                pg_database_size(current_database()) as bytes
        """)
        result = db.execute(query).first()
        print(f"[OK] Database Size: {result.formatted} ({result.bytes} bytes)")
        return result.formatted, result.bytes
    except Exception as e:
        print(f"[FAIL] Database Size Error: {e}")
        return "N/D", 0
    finally:
        db.close()

def get_table_checksum(table_name, columns):
    """
    Genera un hash MD5 unico per l'intero contenuto della tabella.
    L'ORDER BY è fondamentale per garantire il determinismo dell'hash.
    """
    db = SessionLocal()
    try:
        # Concateniamo le colonne in un'unica stringa, ne calcoliamo l'hash riga per riga
        # e infine aggreghiamo tutto in un hash globale.
        columns_joined = ", ".join(columns)
        query = text(f"""
            SELECT md5(string_agg(hash, ''))
            FROM (
                SELECT md5(CAST(({columns_joined}) AS text)) as hash
                FROM {table_name}
                ORDER BY id
            ) as subquery
        """)
        checksum = db.execute(query).scalar()
        print(f"[OK] Checksum {table_name}: {checksum}")
        return checksum
    except Exception as e:
        print(f"[FAIL] Checksum Error for {table_name}: {e}")
        return None
    finally:
        db.close()

def verify_baseline():
    print("\n--- STARTING BASELINE VALIDATION ---")
    
    # 1. Check tecnico (Connettività)
    if not check_service_availability():
        sys.exit(1)
        
    # 2. Check di massa critica (Record minimi)
    if not check_data_volume():
        sys.exit(2)

    # 3. Check di occupazione storage
    get_db_size()

    # 4. Check di Integrità Crittografica (Checksum)
    print("\n--- CALCULATING INTEGRITY CHECKSUMS ---")
    # Definiamo le colonne chiave per ogni tabella per il calcolo dell'impronta digitale
    get_table_checksum("patients", ["id", "name", "tax_code"])
    get_table_checksum("encounters", ["id", "patient_id", "encounter_type"])
    get_table_checksum("clinical_notes", ["id", "encounter_id", "content"])

    print("\n--- BASELINE ESTABLISHED: SYSTEM READY FOR FAULT INJECTION ---")
    sys.exit(0)

if __name__ == "__main__":
    verify_baseline()