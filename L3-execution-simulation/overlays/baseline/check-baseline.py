import requests
import sys
import time

# Configurazione target
API_URL = "http://localhost:8000" # O il nome del servizio K8s: http://ehr-backend:8000
EXPECTED_THRESHOLDS = {
    "patients": 100,        # Minimo accettabile per considerare il sistema "in carico"
    "encounters": 400,      # Esempio basato sul seeding (4 per paziente)
    "clinical_notes": 1000  
}

def check_service_availability():
    """Verifica Condizione 1: Il servizio è raggiungibile e il DB è montato?"""
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
    """Verifica Condizione 2: Il dataset ha la 'massa' critica per il test?"""
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

def verify_baseline():
    print("--- STARTING BASELINE VALIDATION ---")
    if not check_service_availability():
        sys.exit(1) # Exit code 1: System Down
        
    if not check_data_volume():
        sys.exit(2) # Exit code 2: Data Insufficient (Test would be invalid)
        
    print("--- BASELINE ESTABLISHED: SYSTEM READY FOR FAULT INJECTION ---")
    sys.exit(0) # Exit code 0: Success

if __name__ == "__main__":
    verify_baseline()