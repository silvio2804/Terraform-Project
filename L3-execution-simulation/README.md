# Layer 3 – Execution & Simulation
Questo layer implementa l’esecuzione sperimentale degli scenari di valutazione definiti nel Layer 1,
operando sulla baseline del System Under Test (SUT) costruita nel Layer 2.

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
  Gli overlay rappresentano modifiche allo stato baseline per l’esecuzione o l’osservazione.
Non sono scenari: sono blocchi riutilizzabili di configurazione o fault.
La strutturazione in overlays rende riutilizzabili i moduli di iniziezione per più scenari. 
La struttura comprende tre overlay:
- chaos-node-loss: simula la perdita di nodi/pod;
- chaos-data-corruption: simula corruzione di dati;
- chaos-network-partition: isola nodi tra di loro.

- `chaos/`  
  Include template generici per la fault injection (es. Chaos Mesh), separando la definizione tecnica dei fault dalla loro applicazione negli overlay.

- `recovery/`  
  Implementa le strategie di recovery valutate negli scenari.

- `runbooks/`  
  Contiene un runbook per ciascuno scenario di valutazione.  
  Ogni runbook definisce la sequenza operativa che collega baseline, fault injection,
  strategie di recovery e raccolta delle osservazioni.

- `assumption`
Contiene le assunzioni di questo layer.
