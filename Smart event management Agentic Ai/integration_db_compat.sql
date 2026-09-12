-- Integration-only compatibility patch.
-- The integrated SQLAlchemy User model/seed_data contain phone, age and college,
-- while the root schema.sql currently does not.
-- This does NOT replace schema.sql. Run only if those columns are missing.

ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(15);
ALTER TABLE users ADD COLUMN IF NOT EXISTS age INTEGER;
ALTER TABLE users ADD COLUMN IF NOT EXISTS college VARCHAR(150);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'ck_users_age_valid'
    ) THEN
        ALTER TABLE users
        ADD CONSTRAINT ck_users_age_valid
        CHECK (age IS NULL OR (age > 0 AND age < 120));
    END IF;
END $$;
