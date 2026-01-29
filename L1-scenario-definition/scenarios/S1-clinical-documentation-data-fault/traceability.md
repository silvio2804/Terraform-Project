## Tracciabilità

- **Layer 2 – Test Environment**
  - PostgreSQL su Kubernetes
  - Volumi persistenti supportati da NFS
  - Virtualizzazione basata su Proxmox

- **Layer 3 – Execution & Simulation**
  - Stato di Baseline: popolamente del DB con record clinici rappresentativi
  - Esperimento: danneggiamento dei volumi persistenti
  - Strategie di ripristino: ripristino manuale dal backup

- **Layer 4 – Monitoring**
  - Controlli di integrità dei dati
  - Misurazione dei tempi di ripristino
  - Metriche di disponibilità del servizio

- **Layer 5 – Analysis**
  - Compromesso tra completezza e correttezza
  - Confronto delle differenze di ripristino tra le strategie