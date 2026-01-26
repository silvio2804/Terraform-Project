import requests

# Configurazione
BASE_URL = "http://192.168.1.7:30080"
NOMI_PAZIENTI = ["Mario Rossi", "Luca Bianchi", "Giulia Verdi", "Sium Junior", "Elena Neri", "Marco Gialli", "Anna Blu", "Paolo Viola", "Sara Arancioni", "Lorenzo Rosa"]
RECORD_PER_PAZIENTE = 5

def popola_db():
    for nome in NOMI_PAZIENTI:
        print(f"--- Creazione paziente: {nome} ---")
        
        # 1. Creazione paziente con POST
        # Se il server vuole i parametri nell'URL anche in POST, usiamo 'params'
        try:
            res_paziente = requests.post(f"{BASE_URL}/patients", params={"name": nome})
            res_paziente.raise_for_status() 
            
            paziente_data = res_paziente.json()
            paziente_id = paziente_data["id"]
            print(f"Successo! ID: {paziente_id}")

            # 2. Inserimento record con POST
            for i in range(1, RECORD_PER_PAZIENTE + 1):
                contenuto = f"Nota clinica numero {i} per {nome}"
                res_record = requests.post(
                    f"{BASE_URL}/records", 
                    params={"patient_id": paziente_id, "content": contenuto}
                )
                
                if res_record.status_code in [200, 201]: # 201 è lo standard per 'Created'
                    print(f"  > Record {i} inserito.")
                else:
                    print(f"  > Errore record {i}: {res_record.status_code}")

        except Exception as e:
            print(f"Errore durante l'elaborazione di {nome}: {e}")

if __name__ == "__main__":
    popola_db()