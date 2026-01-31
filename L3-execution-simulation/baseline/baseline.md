# Baseline
l’insieme minimo di configurazioni e check che rendono osservabile lo stato operativo normale del sistema, senza modificarlo.

# Numero di record
{
  "patients": 221101,
  "encounters": 884404,
  "clinical_notes": 8844040
}

# Dimensione del DB
ehr=# SELECT pg_size_pretty(pg_database_size(current_database()));
 pg_size_pretty 
----------------
 2292 MB
(1 row)

