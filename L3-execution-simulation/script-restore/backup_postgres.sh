#!/bin/bash

export PGPASSWORD="secret"

BACKUP_DIR="$HOME/postgres-backup"
mkdir -p "$BACKUP_DIR"

pg_dump \
  -v \
  -h 192.168.1.7 \
  -p 30432 \
  -U postgres \
  -Fc \
  ehr > "$BACKUP_DIR/ehr_backup_$(date +%Y%m%d_%H%M).dump" \
  2> ehr_dump.log