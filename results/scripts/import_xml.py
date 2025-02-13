import xml.etree.ElementTree as ET
import psycopg2

# PostgreSQL-Verbindungsdaten
DB_PARAMS = {
    "dbname": "lf8_lets_meet_db",
    "user": "user",
    "password": "secret",
    "host": "localhost",
    "port": "5432"
}

# XML-Datei laden
xml_file = "data/Lets_Meet_Hobbies.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Verbindung zur Datenbank
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# Hobby-Daten speichern
for user in root.findall("user"):
    email = user.find("email").text
    hobbies = [h.text for h in user.findall("hobbies/hobby")]

    # User-ID abrufen
    cur.execute("SELECT user_id FROM Users WHERE email = %s;", (email,))
    user_id_result = cur.fetchone()
    if not user_id_result:
        continue
    user_id = user_id_result[0]

    for hobby in hobbies:
        # Hobby hinzufügen, falls nicht existiert
        cur.execute("""
            INSERT INTO Hobbies (hobby) VALUES (%s)
            ON CONFLICT (hobby) DO NOTHING
            RETURNING hobby_id;
        """, (hobby,))
        
        hobby_id = cur.fetchone()
        if hobby_id is None:
            cur.execute("SELECT hobby_id FROM Hobbies WHERE hobby = %s;", (hobby,))
            hobby_id = cur.fetchone()[0]
        else:
            hobby_id = hobby_id[0]

        # Benutzer-Hobby-Verknüpfung
        cur.execute("""
            INSERT INTO UserHobbies (user_id, hobby_id, priority)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, hobby_id) DO NOTHING;
        """, (user_id, hobby_id, 0))  # Standardpriorität gesetzt

conn.commit()
cur.close()
conn.close()
print("XML-Daten erfolgreich importiert!")