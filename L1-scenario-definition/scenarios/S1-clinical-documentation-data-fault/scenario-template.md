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
- **Categoria primaria:** Data-level fault
- **Categoria secondaria** Application-level fault
- **Stato:** permanente
- **Modalità:** perdita di disponibilità del database EHR

Non specifico ancora il punto preciso di iniezione. (lo faccio nel test-case)

## Effetto osservabile
- processo Clinical Documentation  non disponibile
- crash del pod o blocco delle transazioni (transazioni inconsistenti)
- dati clinici indisponibili o incoerenti

## Impatto
- Servizio del DB non disponibile
- Processo Clinical documentation interrotto

## Condizione di violazione BIA
- **Proprietà CIA compromessa:** Availability
- **Soglia:** Unvailability eccede le soglie temporali definite di 2 minuti

## Assunzioni di scenario
- strategia non è l’oggetto della valutazione, ma una precondizione dell’esperimento (il sistema riesce a rientrare nelle soglie BIA)
- Fallimento dei meccanismi automatici di self-healing
- Backup affidabili disponibili
- Nessun intervento esterno prima dell’inizio dello scenario
- Baseline coerente

## Dimensioni di recovery attivate
- Completezza e Correttezza
- Temporalità

### Fattori che influenzano le dimensioni di recovery 
Tali dimensioni possono esssere influenzate da:
- punto di iniezione;
- carico del sistema;

## Strategie di recovery valutata
- **Strategia:** 

- Isolamento delle risorse, l'istanza del database interessata viene isolata per impedire l'ulteriore propagazione dello stato incoerente;

- Ripristino dal backup, il database viene ripristinato dall'ultimo backup coerente disponibile;

- Verifica dell'integrità, vengono eseguiti controlli post-ripristino per garantire la coerenza logica e la correttezza operativa.

## Output atteso
- Sistema nuovamente disponibile;
- ripristino completo e corretto dei dati clinici entro le soglie BIA;
- Misura del recovery gap.
