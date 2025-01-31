import xml.etree.ElementTree as ET
import psycopg2
from psycopg2 import sql

# PostgreSQL-Verbindung herstellen
def connect_to_db():
    return psycopg2.connect(
        dbname="lf8_lets_meet_db",
        user="user",
        password="secret",
        host="localhost",
        port="5432"
    )

# XML-Daten importieren und in die Datenbank speichern
def import_xml_to_postgres(file_path):
    conn = connect_to_db()
    cursor = conn.cursor()

    tree = ET.parse(file_path)
    root = tree.getroot()

    for user in root.findall("user"):
        email = user.find("email").text
        name_parts = user.find("name").text.split(", ")
        last_name = name_parts[0].strip()
        first_name = name_parts[1].strip() if len(name_parts) > 1 else None

        # Benutzer einfügen oder abrufen
        cursor.execute(
            sql.SQL("""
                INSERT INTO Users (email, first_name, last_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id;
            """),
            (email, first_name, last_name)
        )
        user_id = cursor.fetchone()
        if not user_id:
            cursor.execute("SELECT id FROM Users WHERE email = %s;", (email,))
            user_id = cursor.fetchone()[0]
        else:
            user_id = user_id[0]

        # Hobbys einfügen und verknüpfen
        hobbies = user.find("hobbies").findall("hobby")
        for hobby in hobbies:
            hobby_name = hobby.text.strip()

            # Hobby einfügen oder abrufen
            cursor.execute(
                sql.SQL("""
                    INSERT INTO Hobbies (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                    RETURNING id;
                """),
                (hobby_name,)
            )
            hobby_id = cursor.fetchone()
            if not hobby_id:
                cursor.execute("SELECT id FROM Hobbies WHERE name = %s;", (hobby_name,))
                hobby_id = cursor.fetchone()[0]
            else:
                hobby_id = hobby_id[0]

            # Verknüpfung User-Hobby
            cursor.execute(
                sql.SQL("""
                    INSERT INTO UserHobbies (user_id, hobby_id, priority)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """),
                (user_id, hobby_id, 0)
            )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    xml_file_path = "Lets_Meet_Hobbies.xml"  # Dateipfad anpassen
    print("Importiere XML-Daten in die PostgreSQL-Datenbank...")
    import_xml_to_postgres(xml_file_path)
    print("Datenimport abgeschlossen!")
