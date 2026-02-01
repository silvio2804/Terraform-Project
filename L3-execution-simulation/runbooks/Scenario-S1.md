# Runbook Scenario S1 – Fault su Clinical Documentation

1. scegliere un processo critico ottenuto dalla BIA
2. Deploy baseline
2. Applicare chaos engineering
3. Verificare violazione soglie BIA (triade CIA) sul processo critico
4. Applicare recovery strategy
5. Raccogliere metriche e mapparle nei domini considerati:
   - completezza del recovery
   - correttezza del recovery
   - temporalità del recovery
   - stabilità del recovery
6. misurare il recovery gap, ovvero quanto si discosta la condizione del sistema dalla BIA, dopo aver applicato la strategia
7. determinare se la strategia è sufficiente

## Recovery strategy 

1. check baseline pre-test (check-baseline.py)
2. inietto il fault (dalla dashboard o dalla file .yml)
3. soglie bia violate, automaticamente
4. recovery strategy A
      applico strategy-A.yml
5. osservazione
