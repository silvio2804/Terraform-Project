-- Estensione UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Pazienti (Anagrafica)
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    tax_code TEXT UNIQUE, -- Per rendere la ricerca più realistica
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Encounter (Eventi clinici/Visite)
-- Funge da pivot: collega il paziente al momento temporale
CREATE TABLE IF NOT EXISTS encounters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
    encounter_type TEXT NOT NULL, -- es. EMERGENCY, ROUTINE, INPATIENT
    admitted_at TIMESTAMP NOT NULL,
    discharged_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_encounter_date ON encounters(admitted_at);

-- 3. Clinical Notes (Dati pesanti e strutturati)
CREATE TABLE IF NOT EXISTS clinical_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    encounter_id UUID REFERENCES encounters(id) ON DELETE CASCADE,
    patient_id UUID REFERENCES patients(id), -- Denormalizzazione utile per query veloci
    note_type TEXT NOT NULL, -- es. DIAGNOSIS, PROGRESS_NOTE, DISCHARGE_SUMMARY
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Audit Log (Immutabile per misurare il Recovery Gap)
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    patient_id UUID,
    actor_id TEXT DEFAULT 'system',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indici per simulare performance reali
CREATE INDEX idx_notes_created_at ON clinical_notes(created_at);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);