Passwort-Manager (Python & Tkinter)

Ein einfacher Passwort-Manager in Python, der mit Tkinter eine GUI bereitstellt und mithilfe von Fernet (cryptography) Passwörter sicher verschlüsselt speichert.  
Beim ersten Start wird ein Master-Passwort erstellt, mit dem anschließend alle gespeicherten Zugangsdaten verschlüsselt und wieder entschlüsselt werden.



Features
- Erstellt beim ersten Start ein Master-Passwort
- Speicherung von:
  - Account/Plattform
  - Benutzername/Email
  - Passwort (verschlüsselt)
- Anzeige der gespeicherten Accounts in einer Listbox
- Entschlüsseln und Anzeigen einzelner Passwörter
- Löschen von Einträgen
- Sichere Passwort-Verschlüsselung mit **Fernet**

---

Voraussetzungen
- **Python 3.8+**
- Abhängigkeiten aus `requirements.txt` installieren:

```bash
pip install cryptography
