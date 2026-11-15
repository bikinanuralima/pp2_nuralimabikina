
-- schema.sql

-- 1. Groups
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;


-- 2. Extend existing contacts table
ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100);

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS birthday DATE;

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS group_id INTEGER
REFERENCES groups(id);

ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP;


-- 3. Phones table
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL
        REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL
        CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);


-- 4. Migrate old phone numbers, if the old column exists
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'contacts'
          AND column_name = 'phone'
    ) THEN

        INSERT INTO phones (contact_id, phone, type)
        SELECT id, phone, 'mobile'
        FROM contacts
        WHERE phone IS NOT NULL
          AND phone <> ''
        ON CONFLICT (contact_id, phone) DO NOTHING;

    END IF;
END $$;


-- 5. Indexes
CREATE INDEX IF NOT EXISTS idx_contacts_name
ON contacts(first_name);

CREATE INDEX IF NOT EXISTS idx_contacts_email
ON contacts(email);

CREATE INDEX IF NOT EXISTS idx_phones_phone
ON phones(phone);
