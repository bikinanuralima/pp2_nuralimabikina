


CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE firstname = p_name
    ) THEN

        UPDATE contacts
        SET phone = p_phone
        WHERE firstname = p_name;

    ELSE

        INSERT INTO contacts(firstname, phone)
        VALUES (p_name, p_phone);

    END IF;

END;
$$;





-- =========================================




CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names TEXT[],
    p_phones TEXT[],
    INOUT p_invalid JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN

    p_invalid := '[]'::JSONB;

    IF COALESCE(array_length(p_names, 1), 0)
       <> COALESCE(array_length(p_phones, 1), 0) THEN
        RAISE EXCEPTION 'Names and phones must have equal lengths';
    END IF;

    FOR i IN 1..COALESCE(array_length(p_names, 1), 0) LOOP

        IF p_names[i] IS NULL OR TRIM(p_names[i]) = '' THEN

            p_invalid := p_invalid || jsonb_build_array(
                jsonb_build_object(
                    'name', p_names[i],
                    'phone', p_phones[i],
                    'reason', 'Invalid name'
                )
            );

        ELSIF p_phones[i] IS NULL
           OR p_phones[i] !~ '^\+?[0-9]{10,15}$' THEN

            p_invalid := p_invalid || jsonb_build_array(
                jsonb_build_object(
                    'name', p_names[i],
                    'phone', p_phones[i],
                    'reason', 'Invalid phone'
                )
            );

        ELSE

            BEGIN

                IF EXISTS (
                    SELECT 1
                    FROM contacts
                    WHERE firstname = p_names[i]
                ) THEN

                    UPDATE contacts
                    SET phone = p_phones[i]
                    WHERE firstname = p_names[i];

                ELSE

                    INSERT INTO contacts(firstname, phone)
                    VALUES (p_names[i], p_phones[i]);

                END IF;

            EXCEPTION WHEN unique_violation THEN

                p_invalid := p_invalid || jsonb_build_array(
                    jsonb_build_object(
                        'name', p_names[i],
                        'phone', p_phones[i],
                        'reason', 'Duplicate phone'
                    )
                );

            END;

        END IF;

    END LOOP;

END;
$$;




-- =========================================




CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM contacts
    WHERE firstname = p_value
       OR phone = p_value;

END;
$$;



