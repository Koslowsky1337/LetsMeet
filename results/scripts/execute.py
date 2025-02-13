#!/usr/bin/env python3
import subprocess
import sys

def run_sql():
    # Beispiel: Ausführen der SQL-Datei mit SQLite und der Datenbank "database.db"
    sql_command = "psql -h localhost -p 5432 -U user -d lf8_lets_meet_db -f create_tables.sql"
    print("Führe create_tables.sql aus...")
    result = subprocess.run(sql_command, shell=True)
    if result.returncode != 0:
        print("Fehler beim Ausführen von create_tables.sql", file=sys.stderr)
        sys.exit(result.returncode)
    else:
        print("create_tables.sql erfolgreich ausgeführt.")

def run_script(script_name):
    print(f"Führe {script_name} aus...")
    # Je nach Umgebung ggf. "python3" statt "python" verwenden
    result = subprocess.run(["python", script_name])
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