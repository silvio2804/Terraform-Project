# Scenario S1 – Loss of Availability of Clinical Documentation System

## ID e nome
- **ID:** CD-AV-01
- **Nome:** Loss of Availability of Clinical Documentation System

## Processo aziendale coinvolto
- Clinical Documentation

## Asset coinvolti
- EHR application backend
- Database: PostgreSQL EHR
- Persistent Volumes e worker node (NFS): Kubernetes 

## Fault innescato
- **Categoria primaria:** Infrastructure-Level Fault
- **Stato:** permanente
- **Modalità:** perdita di disponibilità del database EHR

Non specifico ancora il punto preciso di iniezione. (lo faccio nel test-case)

## Effetto osservabile (impatto)
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
- Completezza e Correttezza
- Temporalità

### Fattori che influenzano le dimensioni di recovery 
Tali dimensioni possono esssere influenate da:
- punto di iniezione;
- carico del sistema;

## Strategie di recovery valutate
- **Strategia A:** isolamento asset + restore da backup + verifica integrità

## Output atteso
- Sistema nuovamente disponibile;
- ripristino completo e corretto dei dati clinici entro le soglie BIA;
- Misura del recovery gap.
