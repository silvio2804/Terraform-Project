## Layer 2 - Bulding test environment
Il layer 2 ha come obiettivo la costruizione di un ambiente di simulazione realistico e coerente con il profilo organizzativo. Questo layer deve garantire ripetibilità degli esperimenti e automazione.


## Output del layer 2
L'output è un System Under Test, e rappresenta la baseline del sistema, ovvero lo stato del sistema precedente al fault. La baseline viene congelata,cioè immutabile per tutti gli esperimenti, in modo che vengano effettuati sullo stesso SUT.

## Struttura
Il layer utilizza strumenti di provisioning automatici, sfruttando il paradigma IaC.
La cartella è strutturata come segue:
- terraform, viene utilizzato per il provisioning dell'infrastruttura fisica e virtuale. Il provisioning include VM, rete virtuale, storage.
- ansible, viene utilizzato per configurare l'infrastruttura fornita nella cartella k8s e avviare il cluster Kubernetes;
- k8s, contiene i file di configurazione (manifest) del cluster, avviati da ansible.
- assumption, le assunzioni che verranno utilizzate in questo layer.

