#!/usr/bin/env python3
import subprocess
import sys

# Absoluter Pfad zum Ordner, in dem sich die Skripte und die SQL-Datei befinden.
BASE_PATH = "results/scripts"

def run_sql():
    # Absoluter Pfad zur SQL-Datei
    sql_file = f"{BASE_PATH}/create_tables.sql"
    print("Führe create_tables.sql aus...")
    # Öffne die SQL-Datei und leite ihren Inhalt als stdin an den docker exec Befehl weiter.
    try:
        with open(sql_file, "rb") as f:
            result = subprocess.run(
                ["docker", "exec", "-i", "lf8_lets_meet_postgres_container",
                "psql", "-U", "user", "-d", "lf8_lets_meet_db"],
                stdin=f
            )
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {sql_file}", file=sys.stderr)
        sys.exit(1)
        
    if result.returncode != 0:
        print("Fehler beim Ausführen von create_tables.sql", file=sys.stderr)
        sys.exit(result.returncode)
    else:
        print("create_tables.sql erfolgreich ausgeführt.")

def run_script(script_name):
    # Absoluter Pfad zum Python-Skript
    script_file = f"{BASE_PATH}/{script_name}"
    print(f"Führe {script_name} aus...")
    result = subprocess.run(["python", script_file])
    if result.returncode != 0:
        print(f"Fehler beim Ausführen von {script_name}", file=sys.stderr)
        sys.exit(result.returncode)
    else:
        print(f"{script_name} erfolgreich ausgeführt.")

def main():
    run_sql()
    run_script("import_excel.py")
    run_script("import_mongodb.py")
    run_script("import_xml.py")

if __name__ == "__main__":
    main()
