## Terraform – Provisioning dell'ambiente di test

Terraform viene utilizzato per il provisioning dell'infrastruttura fisica e virtuale
necessaria per ospitare il sistema in fase di test.

Il provisioning include:
- Macchine virtuali su Proxmox
- Configurazione di rete e VLAN
- Risorse di archiviazione per volumi persistenti

Terraform non fa parte della valutazione e viene utilizzato solo per istanziare un ambiente di test riproducibile.

## Ansible – Configurazione del sistema

Ansible viene utilizzato per configurare l'infrastruttura fornita e avviare il cluster Kubernetes.

Ciò include:
- Configurazione del sistema operativo e prerequisiti
- Installazione del runtime del container
- Inizializzazione del cluster Kubernetes
- Configurazione dello storage

I playbook Ansible non implementano l'iniezione di errori, le strategie di ripristino o la logica di test.