# Datenschutzkonzept für die DSGVO-konforme Migration der LetsMeet-Daten

## 1. Einleitung

Dieses Dokument beschreibt das Datenschutzkonzept für die Migration der LetsMeet-Daten (Excel-Dump, MongoDB und XML) in die neue PostgreSQL-Datenbank. Der Migrationsprozess unterliegt den strengen Vorgaben der Datenschutz-Grundverordnung (DSGVO) sowie den ergänzenden Regelungen des Bundesdatenschutzgesetzes (BDSG). Ziel ist es, die personenbezogenen Daten während des gesamten Migrationsprozesses zu schützen, die Rechte der betroffenen Personen zu wahren und alle Verarbeitungsvorgänge transparent und nachvollziehbar zu dokumentieren.

## 2. Geltungsbereich und Zielsetzung

- **Geltungsbereich:**  
  Dieses Konzept gilt ausschließlich für den Migrationsprozess der bestehenden Daten in das Zielsystem (PostgreSQL in einem Docker-Container). Es umfasst alle technischen, organisatorischen und dokumentarischen Maßnahmen, die zur Gewährleistung eines DSGVO-konformen Datenumgangs erforderlich sind.

- **Zielsetzung:**  
  - Sicherstellung der Integrität, Vertraulichkeit und Verfügbarkeit der personenbezogenen Daten während der Migration.  
  - Einhaltung aller relevanten Datenschutzprinzipien und -vorgaben der DSGVO und des BDSG.  
  - Dokumentation und Nachvollziehbarkeit der einzelnen Migrationsschritte, um Rechenschaftspflicht (Accountability) zu gewährleisten.

## 3. Beschreibung der Datenquellen und -arten

Die zu migrierenden Daten liegen in unterschiedlichen Formaten vor:

### 3.1. Excel-Dump
- **Inhalt:**  
  Stammdaten wie Name, Adresse, Telefonnummer, E-Mail, Geschlecht, Geburtsdatum sowie Hobbys (inklusive Prioritäten und Interessen).
- **Besonderheiten:**  
  Mehrere Datenelemente werden in einer Spalte kombiniert (z. B. Vorname, Nachname oder Adresse bestehend aus Straße, Hausnummer, PLZ, Ort).

### 3.2. MongoDB
- **Inhalt:**  
  Benutzerbezogene Informationen wie Likes, Nachrichten, Freundeslisten und Zeitstempel.
- **Besonderheiten:**  
  Die Dokumentenstruktur weicht von einem relationalen Modell ab und erfordert daher eine sorgfältige Datenharmonisierung.

### 3.3. XML-Datei
- **Inhalt:**  
  Ergänzende Hobbys einzelner Benutzer, die mit den Excel-Daten abgeglichen werden müssen.
  
### 3.4. Datenkategorien
Die migrierten Daten umfassen:
- **Stammdaten:** Name, Adresse, Telefonnummer, E-Mail.
- **Profilinformationen:** Geschlecht, Geburtsdatum, Hobbys, Interessen, Profilbilder (später als BLOB gespeichert) sowie zusätzliche Fotos.
- **Kommunikationsdaten:** Nachrichten, Likes, Freundeslisten und zugehörige Zeitstempel.
- **Technische Daten:** Log-Daten und Protokollinformationen, die den Migrationsprozess dokumentieren.

## 4. Datenschutzgrundsätze gemäß DSGVO

Die Verarbeitung der Daten erfolgt unter Einhaltung der folgenden DSGVO-Grundsätze (Art. 5 DSGVO):

- **Rechtmäßigkeit, Verarbeitung nach Treu und Glauben und Transparenz:**  
  Alle Verarbeitungstätigkeiten erfolgen auf einer gesetzlichen Grundlage und werden transparent dokumentiert.

- **Zweckbindung:**  
  Die Daten werden ausschließlich zur Durchführung der Migration verarbeitet und dürfen nicht für andere Zwecke verwendet werden.

- **Datenminimierung:**  
  Es werden nur diejenigen personenbezogenen Daten verarbeitet, die für den Migrationsprozess zwingend erforderlich sind.

- **Richtigkeit:**  
  Es wird sichergestellt, dass die migrierten Daten korrekt und aktuell übernommen werden. Unrichtigkeit ist zeitnah zu korrigieren.

- **Speicherbegrenzung:**  
  Daten werden nur so lange gespeichert, wie es für die Migration erforderlich ist. Nach Abschluss der Migration erfolgt eine Löschung oder Anonymisierung nicht mehr benötigter Daten.

- **Integrität und Vertraulichkeit:**  
  Durch geeignete technische und organisatorische Maßnahmen (TOMs) wird ein angemessenes Schutzniveau vor unbefugtem Zugriff, Verlust oder Manipulation gewährleistet.

- **Rechenschaftspflicht (Accountability):**  
  Alle Verarbeitungsvorgänge werden lückenlos dokumentiert, sodass die Einhaltung der Datenschutzvorgaben jederzeit nachgewiesen werden kann.

## 5. Rechtliche Grundlagen und Verarbeitungsbasis

Die Datenmigration erfolgt ausschließlich auf Grundlage der folgenden Rechtsgrundlagen:

- **Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO):**  
  Die Migration ist notwendig, um den vertraglich vereinbarten Leistungsumfang im Rahmen der Zusammenarbeit mit der LetsMeet GmbH zu gewährleisten.

- **Berechtigtes Interesse (Art. 6 Abs. 1 lit. f DSGVO):**  
  Das berechtigte Interesse an einer sicheren und zuverlässigen Migration der Daten zur Aufrechterhaltung des Betriebs und der IT-Sicherheit wird berücksichtigt.

- **Ergänzende Regelungen des BDSG:**  
  Insbesondere bei besonderen Kategorien personenbezogener Daten werden die Vorgaben des BDSG beachtet.

## 6. Datenschutzrisiken und Datenschutz-Folgenabschätzung (DPIA)

### 6.1. Identifizierte Risiken
- **Unbefugter Zugriff:**  
  Risiko des unautorisierten Zugriffs während des Exports, der Transformation und des Imports der Daten.
- **Datenverlust oder -korruption:**  
  Fehlerhafte Transformationen oder unzureichende Dokumentation können zu Inkonsistenzen führen.
- **Fehlende Nachvollziehbarkeit:**  
  Unvollständige Dokumentation erschwert die Ursachenforschung bei eventuellen Vorfällen.

### 6.2. Datenschutz-Folgenabschätzung (DPIA)
- Gemäß Art. 35 DSGVO wird für den Migrationsprozess eine Datenschutz-Folgenabschätzung durchgeführt, um die Risiken für die Rechte und Freiheiten der betroffenen Personen zu bewerten und geeignete Maßnahmen zur Risikominimierung zu definieren.
- Falls während der DPIA erhöhte Risiken identifiziert werden, werden zusätzliche technische oder organisatorische Maßnahmen implementiert.

## 7. Technische und organisatorische Maßnahmen (TOMs)

Zur Gewährleistung der DSGVO-Konformität werden folgende Maßnahmen ergriffen:

### 7.1. Zugangskontrolle und Berechtigungsmanagement
- **Zugriffsrechte:**  
  Der Zugriff auf die Migrationssysteme, Quell- und Zielsysteme ist ausschließlich autorisierten Mitarbeitern vorbehalten.
- **Authentifizierung:**  
  Einsatz von sicheren Zugangsdaten und, wo möglich, Zwei-Faktor-Authentifizierung für administrative Zugriffe.

### 7.2. Verschlüsselung und sichere Übertragung
- **Datenübertragung:**  
  Alle Daten werden über verschlüsselte Kanäle (z. B. SSL/TLS) übertragen.
- **Datenhaltung:**  
  Temporäre Datenzwischenspeicher und Backups erfolgen in gesicherten und verschlüsselten Systemen.

### 7.3. Versionierung und Dokumentation
- **Git-Versionierung:**  
  Alle SQL-Skripte und Importprogramme werden in einem Git-Repository versioniert und dokumentiert.
- **Transparente Dokumentation:**  
  Jeder Migrationsschritt wird in entsprechenden Markdown-Dokumenten festgehalten, um die Nachvollziehbarkeit zu gewährleisten.

### 7.4. Testläufe und Datenintegritätsprüfungen
- **Testmigrationen:**  
  Vor der finalen Migration werden Testläufe durchgeführt, um die Datenintegrität und -konsistenz sicherzustellen.
- **Audit und Monitoring:**  
  Laufende Überwachung und Protokollierung aller Aktivitäten, um mögliche Unregelmäßigkeiten frühzeitig zu erkennen.

### 7.5. Notfallmanagement
- **Notfallplan:**  
  Es existiert ein definierter Notfallplan, der im Falle eines Datenschutzvorfalls (z. B. Datenleck) schnelle Gegenmaßnahmen vorsieht.

## 8. Rechte der betroffenen Personen

Die DSGVO räumt den betroffenen Personen umfangreiche Rechte zu. Diese werden im Rahmen des Migrationsprozesses wie folgt gewährleistet:

- **Auskunftsrecht:**  
  Betroffene können jederzeit Auskunft über die zu ihrer Person verarbeiteten Daten verlangen.
- **Recht auf Berichtigung:**  
  Unrichtige oder unvollständige Daten werden auf Antrag berichtigt.
- **Recht auf Löschung:**  
  Betroffene haben das Recht, die Löschung ihrer Daten zu verlangen, sofern keine gesetzlichen Aufbewahrungspflichten entgegenstehen.
- **Recht auf Einschränkung der Verarbeitung:**  
  Unter bestimmten Umständen kann die Verarbeitung eingeschränkt werden.
- **Recht auf Datenübertragbarkeit:**  
  Betroffene können verlangen, dass ihre Daten in einem strukturierten, gängigen und maschinenlesbaren Format übermittelt werden.
- **Widerspruchsrecht:**  
  Betroffene können der Verarbeitung ihrer Daten widersprechen, sofern diese auf berechtigten Interessen beruht.
- **Kontakt:**  
  Alle Anfragen und die Ausübung der Rechte richten sich an den unter § 38 BDSG benannten Datenschutzbeauftragten oder den Verantwortlichen (siehe Abschnitt 9).

## 9. Datenminimierung, Zweckbindung und Speicherbegrenzung

- **Datenminimierung:**  
  Es werden ausschließlich die für den Migrationsprozess notwendigen Daten verarbeitet. Nicht relevante oder überflüssige Daten werden nicht migriert.
- **Zweckbindung:**  
  Die Verarbeitung erfolgt ausschließlich zur Durchführung der Migration. Eine Weiterverwendung der Daten zu anderen Zwecken findet nicht statt.
- **Speicherbegrenzung:**  
  Die personenbezogenen Daten werden nur so lange gespeichert, wie es für den Abschluss und die eventuelle Fehlerbehebung der Migration erforderlich ist. Anschließend werden nicht mehr benötigte Daten gemäß den gesetzlichen Vorgaben gelöscht oder anonymisiert.

## 10. Zusammenfassung und Fazit

Dieses Datenschutzkonzept stellt sicher, dass die Migration der LetsMeet-Daten in das neue Zielsystem vollständig DSGVO-konform erfolgt. Durch die konsequente Umsetzung der Datenschutzgrundsätze, die Durchführung einer Datenschutz-Folgenabschätzung, den Einsatz technischer und organisatorischer Maßnahmen sowie die Gewährleistung der Rechte der betroffenen Personen wird ein hohes Schutzniveau gewährleistet. Alle einzelnen Schritte werden detailliert dokumentiert, um eine lückenlose Nachvollziehbarkeit und Rechenschaftspflicht sicherzustellen.

*Ende des Datenschutzkonzepts*
