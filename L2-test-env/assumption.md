# Layer 2 - Assunzioni sull'ambiente
Le seguenti assunzioni definiscono i confini dell'ambiente di test sperimentale
e si applicano a tutti gli scenari.

- L'infrastruttura è implementata su un cluster Proxmox on-premise.
- La connettività di rete tra i nodi è stabile e non degradata,
  a meno che non sia esplicitamente influenzata da uno scenario.
- Il piano di controllo Kubernetes è raggiungibile all'avvio dello scenario.
- Lo storage persistente è fornito tramite volumi supportati da NFS.
- Il database contiene un numero fisso di record EHR
- Sono disponibili backup validi e coerenti dei dati persistenti
  prima dell'iniezione dell'incidente.
- Non si verificano interventi operativi esterni prima dell'esecuzione dello scenario.
- 
I playbook Ansible in questo layer effettuano solo il provisioning del cluster k8s.

Le tecnologie infine non sono oggetto di valuatazione.
