
import csv
from connect import connect, create_table


# 1. Add a contact manually
def add_contact():
    name = input("Enter first name: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not phone:
        print("Name and phone cannot be empty.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# 2. Import contacts from CSV
def import_csv():
    filename = input("Enter CSV filename (default contacts.csv): ").strip()

    if not filename:
        filename = "contacts.csv"

    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or not {
                "first_name", "phone"
            }.issubset(reader.fieldnames):
                print("CSV must have first_name and phone columns.")
                return

            count = 0

            for row in reader:
                name = row["first_name"].strip()
                phone = row["phone"].strip()

                if not name or not phone:
                    continue

                cur.execute(
                    """
                    INSERT INTO contacts (first_name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (name, phone)
                )

                count += cur.rowcount

        conn.commit()
        print("Imported contacts:", count)

    except Exception as e:
        conn.rollback()
        print("Import error:", e)

    finally:
        cur.close()
        conn.close()


# 3. Show all contacts
def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, first_name, phone FROM contacts ORDER BY id"
    )

    contacts = cur.fetchall()

    if contacts:
        print("\nID | First Name | Phone")
        print("-" * 40)

        for contact in contacts:
            print(contact[0], "|", contact[1], "|", contact[2])
    else:
        print("PhoneBook is empty.")

    cur.close()
    conn.close()


# 4. Search contacts by name
def search_by_name():
    name = input("Enter name to search: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, first_name, phone
        FROM contacts
        WHERE first_name ILIKE %s
        ORDER BY id
        """,
        ("%" + name + "%",)
    )

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    if not contacts:
        print("No contacts found.")

    cur.close()
    conn.close()


# 5. Search contacts by phone prefix
def search_by_prefix():
    prefix = input("Enter phone prefix: ").strip()

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, first_name, phone
        FROM contacts
        WHERE phone LIKE %s
        ORDER BY id
        """,
        (prefix + "%",)
    )

    contacts = cur.fetchall()

    for contact in contacts:
        print(contact)

    if not contacts:
        print("No contacts found.")

    cur.close()
    conn.close()


# 6. Update a contact's name or phone
def update_contact():
    contact_id = input("Enter contact ID: ").strip()

    if not contact_id.isdigit():
        print("ID must be a number.")
        return

    print("1. Update first name")
    print("2. Update phone number")

    choice = input("Choose an option: ").strip()

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("Enter new first name: ").strip()

            if not name:
                print("Name cannot be empty.")
                return

            cur.execute(
                """
                UPDATE contacts
                SET first_name = %s
                WHERE id = %s
                RETURNING id
                """,
                (name, int(contact_id))
            )

        elif choice == "2":
            phone = input("Enter new phone number: ").strip()

            if not phone:
                print("Phone cannot be empty.")
                return

            cur.execute(
                """
                UPDATE contacts
                SET phone = %s
                WHERE id = %s
                RETURNING id
                """,
                (phone, int(contact_id))
            )

        else:
            print("Invalid option.")
            return

        if cur.fetchone():
            conn.commit()
            print("Contact updated successfully!")
        else:
            conn.rollback()
            print("Contact ID not found.")

    except Exception as e:
        conn.rollback()
        print("Update error:", e)

    finally:
        cur.close()
        conn.close()


# 7. Delete a contact by name or phone
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone number")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        value = input("Enter first name: ").strip()
        sql = "DELETE FROM contacts WHERE first_name = %s RETURNING id"

    elif choice == "2":
        value = input("Enter phone number: ").strip()
        sql = "DELETE FROM contacts WHERE phone = %s RETURNING id"

    else:
        print("Invalid option.")
        return

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(sql, (value,))
        deleted = cur.fetchall()

        conn.commit()

        if deleted:
            print("Deleted contacts:", len(deleted))
        else:
            print("No matching contact found.")

    except Exception as e:
        conn.rollback()
        print("Delete error:", e)

    finally:
        cur.close()
        conn.close()


# Main menu
def main():
    create_table()

    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Add contact")
        print("2. Import contacts from CSV")
        print("3. Show all contacts")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Update contact")
        print("7. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            import_csv()
        elif choice == "3":
            show_contacts()
        elif choice == "4":
            search_by_name()
        elif choice == "5":
            search_by_prefix()
        elif choice == "6":
            update_contact()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
