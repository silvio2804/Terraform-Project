# Layer 3 – Execution & Simulation

Questo layer implementa l’esecuzione sperimentale degli scenari di valutazione definiti nel Layer 1,
operando sulla baseline del System Under Test (SUT) costruita nel Layer 2.

Il Layer 3 **non modifica né ridefinisce la baseline**: tutte le attività qui contenute sono applicate
come overlay temporanei o come strategie di recovery sullo stesso sistema iniziale controllato.

## Scopo del layer

- Iniettare fault coerenti con gli scenari definiti a livello concettuale
- Applicare e confrontare strategie di recovery
- Orchestrare l’esecuzione sperimentale degli scenari
- Abilitare la raccolta dei dati necessari alla valutazione delle recovery capabilities

## Struttura

- `overlays/`  
  Contiene overlay applicabili alla baseline per l’osservazione iniziale o l’iniezione di fault
  (es. perdita di nodi, corruzione dei dati, partizioni di rete).  
  Gli overlay sono organizzati per tipologia di azione tecnica e sono riutilizzabili tra scenari.

- `chaos/`  
  Include template generici per la fault injection (es. Chaos Mesh), separando la definizione tecnica dei fault dalla loro applicazione negli overlay.

- `recovery/`  
  Implementa le strategie di recovery valutate negli scenari:
  - `manual/`: runbook descrittivi che rappresentano interventi umani
  - `assisted/`: playbook o script di automazione guidata per il ripristino

- `runbooks/`  
  Contiene un runbook per ciascuno scenario di valutazione.  
  Ogni runbook definisce la sequenza operativa che collega baseline, fault injection,
  strategie di recovery e raccolta delle osservazioni.

## Principi di progettazione

- Il Layer 3 **non è suddiviso per scenario** a livello strutturale
- Gli scenari selezionano e combinano overlay e strategie di recovery sullo stesso SUT
- La separazione tra fault, recovery e orchestrazione garantisce riproducibilità e comparabilità
  tra scenari differenti
