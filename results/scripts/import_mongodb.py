import pymongo
import psycopg2
from psycopg2 import sql
from datetime import datetime

# MongoDB-Verbindung herstellen
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["lets_meet_db"]
    return db["users"]

# PostgreSQL-Verbindung herstellen
def connect_to_postgres():
    return psycopg2.connect(
        dbname="lf8_lets_meet_db",
        user="user",
        password="secret",
        host="localhost",
        port="5432"
    )

# Daten aus MongoDB importieren und in PostgreSQL speichern
def import_mongo_to_postgres():
    mongo_collection = connect_to_mongo()
    postgres_conn = connect_to_postgres()
    cursor = postgres_conn.cursor()

    for document in mongo_collection.find():
        email = document.get("_id")
        name_parts = document.get("name", "").split(", ")
        last_name = name_parts[0].strip()
        first_name = name_parts[1].strip() if len(name_parts) > 1 else None
        phone = document.get("phone")

        # Benutzer einfügen oder abrufen
        cursor.execute(
            sql.SQL("""
                INSERT INTO Users (email, first_name, last_name, phone)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id;
            """),
            (email, first_name, last_name, phone)
        )
        user_id = cursor.fetchone()
        if not user_id:
            cursor.execute("SELECT id FROM Users WHERE email = %s;", (email,))
            user_id = cursor.fetchone()[0]
        else:
            user_id = user_id[0]

        # Likes einfügen
        for like in document.get("likes", []):
            liked_email = like.get("liked_email")
            status = like.get("status")
            timestamp = like.get("timestamp")

            # Like verarbeiten
            cursor.execute(
                sql.SQL("""
                    INSERT INTO Likes (user_id, liked_user_id, status, timestamp)
                    VALUES (%s, (SELECT id FROM Users WHERE email = %s), %s, %s)
                    ON CONFLICT DO NOTHING;
                """),
                (user_id, liked_email, status, timestamp)
            )

        # Nachrichten einfügen
        for message in document.get("messages", []):
            conversation_id = message.get("conversation_id")
            receiver_email = message.get("receiver_email")
            message_text = message.get("message")
            timestamp = message.get("timestamp")

            # Nachricht verarbeiten
            cursor.execute(
                sql.SQL("""
                    INSERT INTO Messages (sender_id, receiver_id, conversation_id, message, timestamp)
                    VALUES (%s, (SELECT id FROM Users WHERE email = %s), %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """),
                (user_id, receiver_email, conversation_id, message_text, timestamp)
            )

    postgres_conn.commit()
    cursor.close()
    postgres_conn.close()

if __name__ == "__main__":
    print("Importiere Daten aus MongoDB in die PostgreSQL-Datenbank...")
    import_mongo_to_postgres()
    print("Datenimport abgeschlossen!")
