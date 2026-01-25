#!/bin/bash

# Assicurati di eseguire come root
if [ "$EUID" -ne 0 ]; then
  echo "Per favore esegui come root: sudo $0"
  exit 1
fi

# File hosts
HOSTS_FILE="/etc/hosts"

# Definizione host da aggiungere
declare -A HOSTS=(
  ["master"]="192.168.1.6"
  ["worker1"]="192.168.1.7"
  ["worker2"]="192.168.1.8"
  ["nfs"]="192.168.1.9"
)

for name in "${!HOSTS[@]}"; do
  ip="${HOSTS[$name]}"
  # Controlla se la riga esiste già
  if grep -q -E "^\s*$ip\s+$name\b" "$HOSTS_FILE"; then
    echo "Entry $name ($ip) già presente, salto..."
  else
    echo "Aggiungo $name ($ip) a $HOSTS_FILE"
    echo -e "$ip\t$name" >> "$HOSTS_FILE"
  fi
done

echo "Aggiornamento completato."

#ssh-keygen -t ed25519
chmod 600 .ssh/id_ed25519


sudo dnf install -y epel-release ansible-core
git clone https://github.com/silvio2804/Ansible-repo.git

# Crea la directory .ssh se non esiste e imposta i permessi corretti
mkdir -p ~/.ssh && chmod 700 ~/.ssh

# Definisce il blocco di configurazione
SSH_CONFIG="Host 192.168.1.*
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR"

# Aggiunge al file config senza duplicare se lo script viene eseguito di nuovo
if ! grep -q "Host 192.168.1.\*" ~/.ssh/config 2>/dev/null; then
    echo -e "\n$SSH_CONFIG" >> ~/.ssh/config
    echo "Configurazione aggiunta con successo a ~/.ssh/config"
else
    echo "La configurazione per 192.168.1.* esiste già."
fi

# Imposta i permessi corretti per il file config
chmod 600 ~/.ssh/config