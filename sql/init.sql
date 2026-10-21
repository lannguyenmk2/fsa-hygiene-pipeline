CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.establishments (
    load_id      BIGSERIAL PRIMARY KEY,
    fhrs_id      INTEGER     NOT NULL,
    payload      JSONB       NOT NULL,
    run_date     DATE        NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_raw_est_run
    ON raw.establishments (fhrs_id, run_date);