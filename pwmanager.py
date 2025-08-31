import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import sys
import os
from cryptography.fernet import Fernet
import crypto_utils as cu    # Eigene Hilfsfunktionen für Salt, Key, Verschlüsselung

DATA_FILE = "pwmanager.json" # Datei mit allen Platformen/Passwörtern (verschlüsselt gespeichert)
SALT_FILE = "salt.bin"       # Salt für die Key-Ableitung (PBKDF2 oder ähnliches)

root = tk.Tk()

def get_root():
    # Erlaubt Zugriff auf das Tk-Hauptfenster von außen.
    return root


def load_or_create_salt():
    # Lädt Salt oder erstellt ein neues und speichert es ab.
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        salt = cu.generate_salt()
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt


# Erster Programmstart: Master-Passwort setzen
if not os.path.exists(SALT_FILE):
    master_password = simpledialog.askstring(
        "Neues Master-Passwort",
        "Bitte ein neues Master-Passwort erstellen:",
        show="*"
    )


    # Neues Salt erzeugen und abspeichern
    salt = cu.generate_salt()
    with open(SALT_FILE, "wb") as f:
        f.write(salt)

else:
    # Salt laden, Passwort abfragen und prüfen
    salt = load_or_create_salt()
    while True:
        master_password = simpledialog.askstring("Master-Passwort", "Bitte Master-Passwort eingeben:", show="*")
        if master_password is None:  # Cancel oder X
            root.destroy()
            sys.exit(0)
        if not master_password.strip():  # leer
            messagebox.showwarning("Hinweis", "Bitte ein Master-Passwort eingeben.")
            continue

        try:
            # Schlüssel generieren und Test-Entschlüsselung versuchen
            key = cu.generate_key(master_password, salt)
            fernet = Fernet(key)

            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    daten = json.load(f)
                if daten:
                    # Test: erstes gespeichertes Passwort entschlüsseln
                    cu.decrypt_text(daten[0]["Passwort"], fernet)

            break  # korrektes Passwort = Schleife verlassen
        except Exception:
            # Falsches Passwort = erneute Abfrage
            messagebox.showerror("Fehler", "Falsches Master-Passwort!")



root.deiconify()

# Listbox zur Anzeige aller gespeicherten Einträge
listbox = tk.Listbox(root, width=50, height=10)

# Verschlüsselungs-Key initialisieren
key = cu.generate_key(master_password, salt)
fernet = Fernet(key)


def lade_listbox():
    # Lädt die gespeicherten Einträge aus der JSON-Datei in die Listbox.
    listbox.delete(0, tk.END)

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            daten = json.load(f)
        except json.JSONDecodeError:
            daten = []

    for eintrag in daten:
        listbox.insert(tk.END, f"{eintrag['Platform']} ({eintrag['Benutzername']})")


def passwort_hinzufuegen():
    # Fragt Platform, Benutzername und Passwort ab und speichert das Passwort verschlüsselt in die JSON-Datei.
    platform = simpledialog.askstring("Platform", "Platform:")
    benutzername = simpledialog.askstring("Benutzername", "Benutzername:")
    passwort = simpledialog.askstring("Passwort", "Passwort:", show="*")

    if not platform or not benutzername or not passwort:
        messagebox.showwarning("Fehler", "Alle Felder müssen ausgefüllt werden.")
        return

    # Passwort verschlüsseln
    verschluesselt = cu.encrypt_text(passwort, fernet)

    # Vorhandene Daten laden oder leere Liste anlegen
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                daten = json.load(f)
            except json.JSONDecodeError:
                daten = []
    else:
        daten = []

    daten.append({"Platform": platform, "Benutzername": benutzername, "Passwort": verschluesselt})

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4)

    lade_listbox()
    messagebox.showinfo("Gespeichert", "Passwort wurde erfolgreich gespeichert.")


def get_passwort():
    # Zeigt das entschlüsselte Passwort für den ausgewählten Eintrag.
    auswahl = listbox.curselection()
    if not auswahl:
        messagebox.showwarning("Fehler", "Bitte zuerst einen Eintrag auswählen.")
        return

    index = auswahl[0]

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        daten = json.load(f)

    eintrag = daten[index]
    entschluesselt = cu.decrypt_text(eintrag["Passwort"], fernet)

    messagebox.showinfo("Passwort", f"Platform: {eintrag['Platform']}\n"
                                    f"Benutzername: {eintrag['Benutzername']}\n"
                                    f"Passwort: {entschluesselt}")


def eintrag_löschen():
    # Löscht den ausgewählten Eintrag.
    auswahl = listbox.curselection()
    if not auswahl:
        messagebox.showwarning("Fehler", "Bitte zuerst einen Eintrag auswählen.")
        return

    index = auswahl[0]

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        daten = json.load(f)

    geloescht = daten.pop(index)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4)

    lade_listbox()
    messagebox.showinfo("Gelöscht", f"Eintrag '{geloescht['Platform']}' wurde gelöscht.")
