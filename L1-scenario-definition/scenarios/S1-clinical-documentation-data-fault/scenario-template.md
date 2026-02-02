# Scenario S1 – Clinical Documentation Unavailability Due to Database Failure

## ID e nome
- **ID:** CD-AV-01
- **Nome:** Clinical Documentation Unavailability Due to Database Failure

## Processo aziendale coinvolto
- Clinical Documentation

## Asset coinvolti
- EHR application backend
- Database: PostgreSQL EHR
- Persistent Volumes e worker node (NFS): Kubernetes 

## Fault innescato
- **Categoria primaria:** Data-level fault
- **Categoria secondaria** Application-level fault
- **Stato:** transiente
- **Effetto sul processo:** permanente
- **Modalità:** perdita di disponibilità del database EHR


Non specifico ancora il punto preciso di iniezione. (lo faccio nel test-case)

## Impatto
- processo Clinical Documentation  non disponibile
- crash del pod o blocco delle transazioni (transazioni inconsistenti)
- dati clinici indisponibili o incoerenti

## Condizione di violazione BIA
- **Proprietà CIA primaria compromessa:** Availability
- **Soglia:** Unavailability > 2 minuti
- **Proprietà CIA secondaria compromessa**: Integrity (potential), l'integrità dei dati non può essere garantita dopo il fault, anche se il db ritorna operativo.

## Assunzioni di scenario
- strategia non è l’oggetto della valutazione, ma una precondizione dell’esperimento (il sistema riesce a rientrare nelle soglie BIA)
- Fallimento dei meccanismi automatici di self-healing
- Backup affidabili disponibili
- Nessun intervento esterno prima dell’inizio dello scenario
- Baseline coerente

## Dimensioni di recovery attivate
- Completezza e Correttezza
- Temporalità

## Fattori che influenzano le dimensioni di recovery 
I seguenti fattori sono identificati come potenziali fonti di variabilità che possono influenzare le capacità di recupero osservate. Questi fattori non sono fissi a livello di scenario, ma sono istanziati nella definizione dei casi di test:
- punto di iniezione;
- carico del sistema;

## Strategie di recovery di riferimento
- Isolamento delle risorse, l'istanza del database interessata viene isolata per impedire l'ulteriore propagazione dello stato incoerente;

- Ripristino dal backup, il database viene ripristinato dall'ultimo backup coerente disponibile;

- Verifica dell'integrità, vengono eseguiti controlli post-ripristino per garantire la coerenza logica e la correttezza operativa.

## Output atteso
- Sistema e processo nuovamente disponibile;
- ripristino completo e corretto dei dati clinici entro le soglie BIA;
- Misura del recovery gap, basato sulle dimensioni attivate.
