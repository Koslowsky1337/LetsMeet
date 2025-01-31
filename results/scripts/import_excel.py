import pandas as pd
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

# Excel-Daten einlesen
def load_excel_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Benutzer- und Hobby-Daten importieren
def import_data_to_postgres(data):
    conn = connect_to_db()
    cursor = conn.cursor()

    for _, row in data.iterrows():
        # Benutzer einfügen
        cursor.execute(
            sql.SQL("""
                INSERT INTO Users (email, first_name, last_name, street, house_number, postal_code, city, phone, gender, birthdate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id;
            """),
            (
                row['email'],
                row['first_name'],
                row['last_name'],
                row['street'],
                row['house_number'],
                row['postal_code'],
                row['city'],
                row['phone'],
                row['gender'],
                row['birthdate']
            )
        )
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]

        # Hobbys einfügen und verknüpfen
        hobbies = row['hobbies'].split(';') if 'hobbies' in row and pd.notna(row['hobbies']) else []
        for hobby in hobbies:
            hobby_name, priority = hobby.strip().rsplit('%', 1) if '%' in hobby else (hobby.strip(), 0)
            priority = int(priority) if priority else 0

            # Hobby einfügen oder ID abrufen
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
                (user_id, hobby_id, priority)
            )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    excel_file_path = "Lets Meet DB Dump.xlsx"  # Dateipfad anpassen
    sheet_name = "Sheet1"  # Tabellenblattname anpassen

    print("Lade Excel-Daten...")
    excel_data = load_excel_data(excel_file_path, sheet_name)

    print("Importiere Daten in die PostgreSQL-Datenbank...")
    import_data_to_postgres(excel_data)

    print("Datenimport abgeschlossen!")
