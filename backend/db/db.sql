-- ClinicCare Mini EMR - schema + seed data
-- Written for PostgreSQL. Run this against a fresh database to get a working schema
-- with sample data, independent of whether the FastAPI app has been wired up yet.

CREATE TABLE IF NOT EXISTS practitioners (
    id              SERIAL PRIMARY KEY,
    full_name       VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    role            VARCHAR(50) NOT NULL DEFAULT 'doctor',
    hashed_password VARCHAR(255),
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patients (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    dob         DATE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diagnoses (
    id          SERIAL PRIMARY KEY,
    icd10_code  VARCHAR(10) NOT NULL UNIQUE,
    description VARCHAR(500) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_diagnoses_code ON diagnoses(icd10_code);
CREATE INDEX IF NOT EXISTS idx_diagnoses_description ON diagnoses(description);

CREATE TABLE IF NOT EXISTS consultations (
    id          SERIAL PRIMARY KEY,
    patient_id  INTEGER NOT NULL REFERENCES patients(id),
    note        TEXT NOT NULL,
    created_by  INTEGER NOT NULL REFERENCES practitioners(id),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by  INTEGER REFERENCES practitioners(id),
    updated_at  TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_consultations_patient ON consultations(patient_id);
CREATE INDEX IF NOT EXISTS idx_consultations_created_by ON consultations(created_by);

CREATE TABLE IF NOT EXISTS consultation_diagnoses (
    consultation_id INTEGER NOT NULL REFERENCES consultations(id) ON DELETE CASCADE,
    diagnosis_id    INTEGER NOT NULL REFERENCES diagnoses(id),
    PRIMARY KEY (consultation_id, diagnosis_id)
);
CREATE INDEX IF NOT EXISTS idx_consultation_diagnoses_diagnosis ON consultation_diagnoses(diagnosis_id);

CREATE TABLE IF NOT EXISTS audit_logs (
    id           SERIAL PRIMARY KEY,
    table_name   VARCHAR(50) NOT NULL,
    record_id    INTEGER NOT NULL,
    action       VARCHAR(10) NOT NULL,  -- CREATE | UPDATE | DELETE
    performed_by INTEGER NOT NULL REFERENCES practitioners(id),
    performed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    old_data     TEXT,  -- JSON snapshot before the change
    new_data     TEXT   -- JSON snapshot after the change
);
CREATE INDEX IF NOT EXISTS idx_audit_logs_record ON audit_logs(table_name, record_id);

-- Sample practitioner for local testing / manual audit checks
INSERT INTO practitioners (full_name, email, role) VALUES ('Dr. Tuan Le', 'tuanle@cliniccare.com', 'doctor')
ON CONFLICT (email) DO NOTHING;

