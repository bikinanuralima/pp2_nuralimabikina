
import csv
import json
import psycopg2

from connect import connect


# --------------------------------
# DATABASE HELPER FUNCTIONS
# --------------------------------

def get_group_id(cur, group_name):
    if not group_name:
        return None

    cur.execute(
        """
        INSERT INTO groups (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (group_name,)
    )

    cur.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    return cur.fetchone()[0]


def find_contact(cur, name):
    cur.execute(
        """
        SELECT id
        FROM contacts
        WHERE LOWER(firstname) = LOWER(%s)
        ORDER BY id
        LIMIT 1
        """,
        (name,)
    )

    result = cur.fetchone()

    if result:
        return result[0]

    return None


def save_contact(cur, contact):
    name = contact["firstname"]
    email = contact.get("email") or None
    birthday = contact.get("birthday") or None
    group_name = contact.get("group")

    group_id = get_group_id(cur, group_name)

    contact_id = find_contact(cur, name)

    if contact_id:
        # Update existing contact
        cur.execute(
            """
            UPDATE contacts
            SET email = %s,
                birthday = %s,
                group_id = %s
            WHERE id = %s
            """,
            (email, birthday, group_id, contact_id)
        )

    else:
        # Insert new contact
        cur.execute(
            """
            INSERT INTO contacts
                (firstname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, email, birthday, group_id)
        )

        contact_id = cur.fetchone()[0]

    # Add phone numbers
    for phone_info in contact.get("phones", []):

        cur.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone) DO NOTHING
            """,
            (
                contact_id,
                phone_info["phone"],
                phone_info["type"]
            )
        )

    return contact_id


# --------------------------------
# DISPLAY CONTACTS
# --------------------------------

def show_contacts(query, params=()):

    conn = connect()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:

            cur.execute(query, params)

            contacts = cur.fetchall()

            if not contacts:
                print("No contacts found.")
                return

            for contact in contacts:
                print("-" * 40)

                for column, value in zip(
                    [desc[0] for desc in cur.description],
                    contact
                ):
                    print(f"{column}: {value}")

            print("-" * 40)

    except psycopg2.Error as e:
        print("Database error:", e)

    finally:
        conn.close()


# --------------------------------
# SEARCH CONTACTS
# --------------------------------

def search_contacts():

    query = input("Enter name, email or phone: ")

    conn = connect()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:

            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (query,)
            )

            results = cur.fetchall()

            if not results:
                print("No contacts found.")
                return

            for contact in results:
                print("-" * 40)
                print("ID:", contact[0])
                print("Name:", contact[1])
                print("Email:", contact[2])
                print("Birthday:", contact[3])
                print("Group:", contact[4])
                print("Phones:", contact[5])

    except psycopg2.Error as e:
        print("Search error:", e)

    finally:
        conn.close()


# --------------------------------
# FILTER BY GROUP
# --------------------------------

def filter_by_group():

    group_name = input("Enter group name: ")

    show_contacts(
        """
        SELECT
            c.id,
            c.firstname,
            c.email,
            c.birthday,
            g.name AS group_name,
            STRING_AGG(p.phone, ', ') AS phones
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, c.firstname, c.email,
                 c.birthday, g.name
        ORDER BY c.firstname
        """,
        (group_name,)
    )


# --------------------------------
# SEARCH BY EMAIL
# --------------------------------

def search_by_email():

    email = input("Enter email or part of email: ")

    show_contacts(
        """
        SELECT
            c.id,
            c.firstname,
            c.email,
            c.birthday,
            g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.firstname
        """,
        ("%" + email + "%",)
    )


# --------------------------------
# SORT CONTACTS
# --------------------------------

def sort_contacts():

    print("\nSort contacts by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    sort_options = {
        "1": "c.firstname ASC",
        "2": "c.birthday ASC NULLS LAST",
        "3": "c.created_at DESC"
    }

    if choice not in sort_options:
        print("Invalid choice.")
        return

    order = sort_options[choice]

    show_contacts(
        f"""
        SELECT
            c.id,
            c.firstname,
            c.email,
            c.birthday,
            c.created_at,
            g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order}
        """
    )


# --------------------------------
# PAGINATION
# --------------------------------

def pagination():

    page = 0
    page_size = 5

    while True:

        offset = page * page_size

        conn = connect()

        if conn is None:
            return

        try:
            with conn.cursor() as cur:

                # Uses the pagination function from Practice 8.
                cur.execute(
                    """
                    SELECT *
                    FROM get_contacts_paginated(%s, %s)
                    """,
                    (page_size, offset)
                )

                results = cur.fetchall()

                if not results:
                    print("No contacts on this page.")

                else:
                    print("\nPAGE", page + 1)
                    print("=" * 40)

                    columns = [
                        description[0]
                        for description in cur.description
                    ]

                    for contact in results:
                        for column, value in zip(
                            columns, contact
                        ):
                            print(f"{column}: {value}")

                        print("-" * 40)

        except psycopg2.Error as e:
            print("Pagination error:", e)

        finally:
            conn.close()

        print("\nnext / prev / quit")

        command = input("Enter command: ").lower()

        if command == "next":
            page += 1

        elif command == "prev":
            if page > 0:
                page -= 1
            else:
                print("Already on the first page.")

        elif command == "quit":
            break

        else:
            print("Invalid command.")


# --------------------------------
# EXPORT CONTACTS TO JSON
# --------------------------------

def export_json():

    conn = connect()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    c.id,
                    c.firstname,
                    c.email,
                    c.birthday,
                    g.name AS group_name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.id
                """
            )

            contacts = cur.fetchall()

            exported = []

            for contact in contacts:

                contact_id = contact[0]

                cur.execute(
                    """
                    SELECT phone, type
                    FROM phones
                    WHERE contact_id = %s
                    ORDER BY id
                    """,
                    (contact_id,)
                )

                phones = cur.fetchall()

                exported.append({
                    "firstname": contact[1],
                    "email": contact[2],
                    "birthday": (
                        contact[3].isoformat()
                        if contact[3] else None
                    ),
                    "group": contact[4],
                    "phones": [
                        {
                            "phone": phone[0],
                            "type": phone[1]
                        }
                        for phone in phones
                    ]
                })

        with open(
            "contacts.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                exported,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("Contacts exported successfully!")

    except (psycopg2.Error, OSError) as e:
        print("Export error:", e)

    finally:
        conn.close()


# --------------------------------
# IMPORT CONTACTS FROM JSON
# --------------------------------

def import_json():

    try:
        with open(
            "contacts.json",
            "r",
            encoding="utf-8"
        ) as file:

            contacts = json.load(file)

        if not isinstance(contacts, list):
            print("JSON must contain a list of contacts.")
            return

    except (OSError, json.JSONDecodeError) as e:
        print("File error:", e)
        return

    conn = connect()

    if conn is None:
        return

    try:
        with conn:

            with conn.cursor() as cur:

                for contact in contacts:

                    if not contact.get("first_name"):
                        print("Skipping contact without a name.")
                        continue

                    contact_id = find_contact(
                        cur,
                        contact["firstname"]
                    )

                    if contact_id:

                        print(
                            "\nContact already exists:",
                            contact["firstname"]
                        )

                        choice = input(
                            "Skip or overwrite? (s/o): "
                        ).lower()

                        if choice == "s":
                            print("Skipped.")
                            continue

                        elif choice == "o":

                            cur.execute(
                                """
                                DELETE FROM phones
                                WHERE contact_id = %s
                                """,
                                (contact_id,)
                            )

                            cur.execute(
                                """
                                UPDATE contacts
                                SET email = %s,
                                    birthday = %s,
                                    group_id = %s
                                WHERE id = %s
                                """,
                                (
                                    contact.get("email") or None,
                                    contact.get("birthday") or None,
                                    get_group_id(
                                        cur,
                                        contact.get("group")
                                    ),
                                    contact_id
                                )
                            )

                        else:
                            print("Invalid choice. Skipped.")
                            continue

                    else:
                        contact_id = None

                    save_contact(cur, contact)

                    print(
                        "Imported:",
                        contact["firstname"]
                    )

        print("\nJSON import completed!")

    except (psycopg2.Error, KeyError, TypeError, ValueError) as e:
        print("Import error:", e)

    finally:
        conn.close()


# --------------------------------
# EXTENDED CSV IMPORT
# --------------------------------

import os

def import_csv(filename="contacts.csv"):
    filename = os.path.join(os.path.dirname(__file__), filename)

    conn = connect()

    if conn is None:
        return

    try:
        with open(
            filename,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            with conn:

                with conn.cursor() as cur:

                    for row in reader:

                        contact = {
                            "firstname": row["firstname"],
                            "email": row.get("email") or None,
                            "birthday": row.get("birthday") or None,
                            "group": row.get("group") or None,
                            "phones": []
                        }

                        phone = row.get("phone", "").strip()

                        if phone:
                            contact["phones"].append({
                                "phone": phone,
                                "type": (
                                    row.get("phone_type") or "mobile"
                                ).lower()
                            })

                        save_contact(cur, contact)

        print("CSV imported successfully!")

    except (OSError, KeyError, psycopg2.Error, ValueError) as e:
        print("CSV import error:", e)

    finally:
        conn.close()


# --------------------------------
# ADD PHONE USING PROCEDURE
# --------------------------------

def add_phone():

    name = input("Contact name: ")
    phone = input("Phone number: ")
    phone_type = input(
        "Type (home/work/mobile): "
    ).lower()

    conn = connect()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:

            cur.execute(
                "CALL add_phone(%s, %s, %s)",
                (name, phone, phone_type)
            )

        conn.commit()
        print("Phone added successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)

    finally:
        conn.close()


# --------------------------------
# MOVE CONTACT USING PROCEDURE
# --------------------------------

def move_to_group():

    name = input("Contact name: ")
    group = input("New group: ")

    conn = connect()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:

            cur.execute(
                "CALL move_to_group(%s, %s)",
                (name, group)
            )

        conn.commit()
        print("Contact moved successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)

    finally:
        conn.close()


# --------------------------------
# MAIN MENU
# --------------------------------

def main():

    while True:

        print("\n========== PHONEBOOK ==========")
        print("1. Search contacts")
        print("2. Filter by group")
        print("3. Search by email")
        print("4. Sort contacts")
        print("5. Navigate pages")
        print("6. Export to JSON")
        print("7. Import from JSON")
        print("8. Import from CSV")
        print("9. Add phone number")
        print("10. Move contact to group")
        print("0. Exit")
        print("===============================")

        choice = input("Choose an option: ")

        if choice == "1":
            search_contacts()

        elif choice == "2":
            filter_by_group()

        elif choice == "3":
            search_by_email()

        elif choice == "4":
            sort_contacts()

        elif choice == "5":
            pagination()

        elif choice == "6":
            export_json()

        elif choice == "7":
            import_json()

        elif choice == "8":
            import_csv()

        elif choice == "9":
            add_phone()

        elif choice == "10":
            move_to_group()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
