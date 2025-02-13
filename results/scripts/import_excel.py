import pandas as pd
import psycopg2
import re
from psycopg2 import sql
from datetime import datetime

# PostgreSQL-Verbindungsdaten
DB_PARAMS = {
    "dbname": "lf8_lets_meet_db",
    "user": "user",
    "password": "secret",
    "host": "localhost",
    "port": "5432"
}

# Lade die Excel-Datei
file_path = "data/Lets Meet DB Dump.xlsx"
df = pd.read_excel(file_path)

# Spalten formatieren: Namen splitten und Adresse extrahieren
df[['last_name', 'first_name']] = df['Nachname, Vorname'].str.split(', ', expand=True)
df[['street', 'house_number', 'postal_code', 'city']] = df['Straße Nr, PLZ Ort'].str.extract(r'(.+?) (\d+), (\d+), (.+)')

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

for _, row in df.iterrows():
    # Adresse speichern und address_id abrufen
    cur.execute("""
        INSERT INTO Addresses (street, house_number, postal_code, city)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING address_id;
    """, (row['street'], row['house_number'], row['postal_code'], row['city']))
    
    address_id = cur.fetchone()
    if address_id is None:
        cur.execute("""
            SELECT address_id FROM Addresses 
            WHERE street = %s AND house_number = %s AND postal_code = %s AND city = %s
        """, (row['street'], row['house_number'], row['postal_code'], row['city']))
        address_id = cur.fetchone()[0]
    else:
        address_id = address_id[0]

    # Konvertiere das Datum ins richtige Format
    birthdate_str = row['Geburtsdatum']
    try:
        birth_date = datetime.strptime(birthdate_str, "%d.%m.%Y").date()
    except Exception as e:
        print(f"Fehler beim Parsen des Datums {birthdate_str}: {e}")
        continue

    # Benutzer speichern und user_id abrufen
    cur.execute("""
        INSERT INTO Users (email, first_name, last_name, address_id, phone, gender, interested_in, birthdate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING
        RETURNING user_id;
    """, (row['E-Mail'], row['first_name'], row['last_name'], address_id, row['Telefon'],
        row['Geschlecht (m/w/nonbinary)'], row['Interessiert an'], birth_date))
    
    user_id = cur.fetchone()
    if user_id is None:
        cur.execute("SELECT user_id FROM Users WHERE email = %s;", (row['E-Mail'],))
        user_id = cur.fetchone()[0]
    else:
        user_id = user_id[0]

    # Hobbies importieren (angenommener Spaltenname – bitte bei Bedarf anpassen)
    hobby_data = row.get('Hobby1 %Prio1%; Hobby2 %Prio2%; Hobby3 %Prio3%; Hobby4 %Prio4%; Hobby5 %Prio5%;')
    if pd.notna(hobby_data):
        hobbies = hobby_data.split(';')
        for hobby_item in hobbies:
            hobby_item = hobby_item.strip()
            if not hobby_item:
                continue
            # Extrahiere Hobbyname und Priorität (Priorität kann auch negativ sein)
            match = re.match(r'(.+?)\s*%(-?\d+)%', hobby_item)
            if match:
                hobby_name = match.group(1).strip()
                priority = int(match.group(2))
            else:
                hobby_name = hobby_item
                priority = 0

            # Hobby in Tabelle Hobbies einfügen und hobby_id abrufen
            cur.execute("""
                INSERT INTO Hobbies (hobby)
                VALUES (%s)
                ON CONFLICT (hobby) DO NOTHING
                RETURNING hobby_id;
            """, (hobby_name,))
            hobby_id = cur.fetchone()
            if hobby_id is None:
                cur.execute("SELECT hobby_id FROM Hobbies WHERE hobby = %s;", (hobby_name,))
                hobby_id = cur.fetchone()[0]
            else:
                hobby_id = hobby_id[0]

            # Benutzer-Hobby-Verknüpfung in UserHobbies einfügen
            cur.execute("""
                INSERT INTO UserHobbies (user_id, hobby_id, priority)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, hobby_id) DO NOTHING;
            """, (user_id, hobby_id, priority))

conn.commit()
cur.close()
conn.close()
print("Excel-Daten erfolgreich importiert!")