# Runbook Scenario S1 – Fault su Clinical Documentation

1. Deploy baseline overlay
2. Applicare overlay chaos-data-corruption
3. Verificare violazione soglie BIA
4. Applicare recovery strategy A
5. Applicare recovery strategy B 
6. Raccogliere metriche su:
   - completezza del recovery
   - correttezza del recovery
   - temporalità del recovery
   - stabilità del recovery

## Recovery strategy A

## Recovery strategy B

1. check baseline pre-test (check-baseline.py)
2. inietto il fault (dalla dashboard o dalla file .yml)
3. soglie bia violate, automaticamente
4. recovery strategy A
      applico strategy-A.yml
5. osservazione
