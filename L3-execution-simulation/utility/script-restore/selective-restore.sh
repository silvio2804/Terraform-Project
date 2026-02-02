#!/bin/bash
set -euo pipefail

# === CONFIG ===
POSTGRES_HOST="192.168.1.7"
POSTGRES_PORT="30032"
POSTGRES_USER="postgres"
POSTGRES_DB="secret"
BACKUP_FILE="$1"   # passato come argomento

LOG_DIR="$HOME/postgres-restore"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/restore_$(date +%Y%m%d_%H%M%S).log"

# === CHECK ===
if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Backup file not found: $BACKUP_FILE" | tee -a "$LOG_FILE"
  exit 1
fi

echo "Starting restore from $BACKUP_FILE" | tee -a "$LOG_FILE"
date | tee -a "$LOG_FILE"

# === RESTORE ===
time pg_restore -v \
  -h "$POSTGRES_HOST" \
  -p "$POSTGRES_PORT" \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  --clean \
  --if-exists \
  "$BACKUP_FILE" \
  2>> "$LOG_FILE"

date | tee -a "$LOG_FILE"
echo "Restore completed successfully" | tee -a "$LOG_FILE"
[silvio@ansible ~]$ 
[silvio@ansible ~]$ ls
Ansible-repo        configAnsible.sh  full_restore.sh  restore_critical.list
backup_postgres.sh  ehr_dump.log      postgres-backup  selective_restore.sh
[silvio@ansible ~]$ cat selective_restore.sh 
#!/bin/bash
set -euo pipefail

# === CONFIG ===
POSTGRES_HOST="192.168.1.7"
POSTGRES_PORT="30432"
POSTGRES_USER="postgres"
POSTGRES_DB="secret"
BACKUP_FILE="$1"   # passato come argomento

LOG_DIR="$HOME/postgres-selective-restore"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/selective_restore_$(date +%Y%m%d_%H%M%S).log"

# === CHECK ===
if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Backup file not found: $BACKUP_FILE" | tee -a "$LOG_FILE"
  exit 1
fi

echo "Starting selective restore from $BACKUP_FILE" | tee -a "$LOG_FILE"
date | tee -a "$LOG_FILE"

# === RESTORE ===
time pg_restore -v \
  -h "$POSTGRES_HOST" \
  -p "$POSTGRES_PORT" \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  --clean \
  --if-exists \
  -L restore_critical.list \
  "$BACKUP_FILE" \
  2>> "$LOG_FILE"

date | tee -a "$LOG_FILE"
echo "Selective Restore completed successfully" | tee -a "$LOG_FILE