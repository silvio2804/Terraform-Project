# Scenario S1 – Fault su Clinical Documentation

## ID e nome
- **ID:** S1
- **Nome:** Fault su Clinical Documentation

## Processo aziendale coinvolto
- Clinical Documentation

## Asset coinvolti
- Database: PostgreSQL EHR
- Persistent Volumes e worker node: Kubernetes 
- storage NFS dedicato della VM: Proxmox server

## Fault innescato
- **Categoria primaria:** Infrastructure-Level Fault
- **Stato:** permanente
- **Modalità:** I/O failure sul volume persistente del database

## Effetto osservabile
- errori I/O su postgresSQL
- crash del pod o blocco delle transazioni
- dati clinici indisponibili o incoerenti

## Condizione di violazione BIA
- **Proprietà CIA compromessa:** Integrity, Availability
- **Soglia:** disponibilità dati 2 minuti perdita o corruzione di dati clinici necessari al completamento della documentazione

## Assunzioni di scenario
- Fallimento dei meccanismi automatici di self-healing
- Backup affidabili disponibili
- Nessun intervento esterno prima dell’inizio dello scenario

## Dimensioni di recovery attivate
- Completezza
- Correttezza
- Temporalità
- Autonomia
- Stabilità

## Strategie di recovery valutate
- **Strategia A:** isolamento asset + restore da backup + verifica integrità
- **Strategia B:** restore selettivo + validazione automatica

## Output atteso
- Sistema nuovamente disponibile;
- ripristino completo e corretto dei dati clinici entro le soglie BIA
- Confronto del recovery gap tra le strategie.
