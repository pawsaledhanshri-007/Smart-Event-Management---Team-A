-- =====================================================================
-- Agentic AI Smart Event Management System — PostgreSQL Schema
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE TABLE users (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR(100)  NOT NULL,
    email          VARCHAR(255)  NOT NULL,
    password_hash  VARCHAR(255)  NOT NULL,
    role           VARCHAR(20)   NOT NULL DEFAULT 'participant',
    is_active      BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ,

    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT ck_users_role_valid CHECK (role IN ('admin', 'organizer', 'participant'))
);

CREATE TABLE venues (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(150)  NOT NULL,
    location    VARCHAR(255),
    capacity    INTEGER       NOT NULL,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now(),
    CONSTRAINT ck_venues_capacity_positive CHECK (capacity > 0)
);

CREATE TABLE events (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title          VARCHAR(200)  NOT NULL,
    description    TEXT,
    venue_id       UUID          NOT NULL,
    organizer_id   UUID          NOT NULL,
    start_time     TIMESTAMPTZ   NOT NULL,
    end_time       TIMESTAMPTZ   NOT NULL,
    capacity       INTEGER       NOT NULL,
    status         VARCHAR(20)   NOT NULL DEFAULT 'scheduled',
    created_at     TIMESTAMPTZ   NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ,

    CONSTRAINT fk_events_venue
        FOREIGN KEY (venue_id) REFERENCES venues (id) ON DELETE RESTRICT,
    CONSTRAINT fk_events_organizer
        FOREIGN KEY (organizer_id) REFERENCES users (id) ON DELETE RESTRICT,
    CONSTRAINT ck_events_time_order CHECK (end_time > start_time),
    CONSTRAINT ck_events_capacity_positive CHECK (capacity > 0),
    CONSTRAINT ck_events_status_valid
        CHECK (status IN ('scheduled', 'ongoing', 'completed', 'cancelled'))
);

CREATE INDEX ix_events_venue_id ON events (venue_id);
CREATE INDEX ix_events_organizer_id ON events (organizer_id);
CREATE INDEX ix_events_start_time ON events (start_time);
CREATE INDEX ix_events_venue_time_range ON events (venue_id, start_time, end_time);

CREATE TABLE registrations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID          NOT NULL,
    event_id        UUID          NOT NULL,
    status          VARCHAR(20)   NOT NULL DEFAULT 'confirmed',
    registered_at   TIMESTAMPTZ   NOT NULL DEFAULT now(),
    cancelled_at    TIMESTAMPTZ,

    CONSTRAINT fk_registrations_user
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_registrations_event
        FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE,
    CONSTRAINT uq_user_event_registration UNIQUE (user_id, event_id),
    CONSTRAINT ck_registrations_status_valid
        CHECK (status IN ('confirmed', 'cancelled', 'waitlisted'))
);

CREATE INDEX ix_registrations_event_id ON registrations (event_id);
CREATE INDEX ix_registrations_user_id ON registrations (user_id);

CREATE TABLE agent_sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID          NOT NULL,
    started_at  TIMESTAMPTZ   NOT NULL DEFAULT now(),
    ended_at    TIMESTAMPTZ,
    CONSTRAINT fk_agent_sessions_user
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX ix_agent_sessions_user_id ON agent_sessions (user_id);

CREATE TABLE agent_runs (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id       UUID          NOT NULL,
    user_message     TEXT          NOT NULL,
    intent           VARCHAR(50),
    final_response   TEXT,
    latency_ms       INTEGER,
    created_at       TIMESTAMPTZ   NOT NULL DEFAULT now(),
    CONSTRAINT fk_agent_runs_session
        FOREIGN KEY (session_id) REFERENCES agent_sessions (id) ON DELETE CASCADE,
    CONSTRAINT ck_agent_runs_latency_nonneg CHECK (latency_ms IS NULL OR latency_ms >= 0)
);

CREATE INDEX ix_agent_runs_session_id ON agent_runs (session_id);
CREATE INDEX ix_agent_runs_created_at ON agent_runs (created_at);

CREATE TABLE tool_calls (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id        UUID          NOT NULL,
    tool_name     VARCHAR(100)  NOT NULL,
    tool_input    JSONB,
    tool_output   JSONB,
    error         TEXT,
    latency_ms    INTEGER,
    created_at    TIMESTAMPTZ   NOT NULL DEFAULT now(),
    CONSTRAINT fk_tool_calls_run
        FOREIGN KEY (run_id) REFERENCES agent_runs (id) ON DELETE CASCADE,
    CONSTRAINT ck_tool_calls_latency_nonneg CHECK (latency_ms IS NULL OR latency_ms >= 0)
);

CREATE INDEX ix_tool_calls_run_id ON tool_calls (run_id);
CREATE INDEX ix_tool_calls_tool_name ON tool_calls (tool_name);

CREATE TABLE knowledge_documents (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title        VARCHAR(255)  NOT NULL,
    source_path  VARCHAR(500),
    created_at   TIMESTAMPTZ   NOT NULL DEFAULT now()
);

CREATE TABLE knowledge_chunks (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id   UUID          NOT NULL,
    chunk_index   INTEGER       NOT NULL,
    content       TEXT          NOT NULL,
    embedding     VECTOR(1536)  NOT NULL,
    CONSTRAINT fk_knowledge_chunks_document
        FOREIGN KEY (document_id) REFERENCES knowledge_documents (id) ON DELETE CASCADE,
    CONSTRAINT uq_document_chunk_index UNIQUE (document_id, chunk_index)
);

CREATE INDEX ix_knowledge_chunks_document_id ON knowledge_chunks (document_id);

CREATE TABLE audit_logs (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id      UUID,
    action        VARCHAR(100)  NOT NULL,
    entity_type   VARCHAR(50),
    entity_id     UUID,
    details       JSONB,
    created_at    TIMESTAMPTZ   NOT NULL DEFAULT now(),
    CONSTRAINT fk_audit_logs_actor
        FOREIGN KEY (actor_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX ix_audit_logs_actor_id ON audit_logs (actor_id);
CREATE INDEX ix_audit_logs_entity ON audit_logs (entity_type, entity_id);
CREATE INDEX ix_audit_logs_created_at ON audit_logs (created_at);
