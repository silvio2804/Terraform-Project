# Scenario S1 – Fault su Clinical Documentation

## ID e nome
- **ID:** S1
- **Nome:** Fault su Clinical Documentation

## Processo aziendale coinvolto
- Clinical Documentation

## Asset coinvolti
- PostgreSQL EHR database
- Kubernetes Persistent Volumes e worker node
- Proxmox server e storage NFS dedicato

## Fault innescato
- **Categoria primaria:** Data-Level Fault
- **Stato:** permanente
- **Modalità:** corruzione, perdita o indisponibilità dei dati clinici persistenti

## Condizione di violazione BIA
- **Proprietà CIA compromessa:** Integrity, Availability
- **Soglia:** perdita o corruzione di dati clinici necessari al completamento della documentazione

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
Ripristino completo e corretto dei dati clinici entro le soglie BIA, con confronto del recovery gap tra le strategie.
