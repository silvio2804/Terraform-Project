## Principi di progettazione

- Il Layer 3 **non è suddiviso per scenario** a livello strutturale
- Gli scenari selezionano e combinano overlay e strategie di recovery sullo stesso SUT
- La separazione tra fault, recovery e orchestrazione garantisce riproducibilità e comparabilità tra scenari differenti

Il Layer 3 **non modifica né ridefinisce la baseline**: tutte le attività qui contenute sono applicate
come overlay temporanei o come strategie di recovery sullo stesso sistema iniziale controllato.