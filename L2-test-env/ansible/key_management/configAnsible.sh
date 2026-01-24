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

