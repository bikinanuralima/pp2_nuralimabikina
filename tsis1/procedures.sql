#1

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name) = LOWER(p_contact_name)
    ORDER BY id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type';
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO NOTHING;

END;
$$;


-- Example:
CALL add_phone('Alex', '87001234567', 'mobile');


#2

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name) = LOWER(p_contact_name)
    ORDER BY id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;

END;
$$;


-- Example:
CALL move_to_group('Alex', 'Friend');

#3


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone_numbers TEXT
)
LANGUAGE sql
AS $$
    SELECT
        c.id,
        c.first_name,
        c.email,
        c.birthday,
        g.name,

        COALESCE(
            STRING_AGG(
                p.phone || ' (' || p.type || ')',
                ', '
            ),
            'No phone'
        )

    FROM contacts c

    LEFT JOIN groups g
        ON c.group_id = g.id

    LEFT JOIN phones p
        ON c.id = p.contact_id

    WHERE
        c.first_name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR EXISTS (
            SELECT 1
            FROM phones p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || p_query || '%'
        )

    GROUP BY
        c.id,
        c.first_name,
        c.email,
        c.birthday,
        g.name

    ORDER BY c.first_name;
$$;


-- Example:
SELECT * FROM search_contacts('gmail');
SELECT * FROM search_contacts('8700');
SELECT * FROM search_contacts('Alex');
