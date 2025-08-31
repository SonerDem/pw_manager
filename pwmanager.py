import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import sys
import os
from cryptography.fernet import Fernet
import crypto_utils as cu  # Kryptofunktionen

DATA_FILE = "pwmanager.json"
SALT_FILE = "salt.bin"

root = tk.Tk()
root.withdraw()

def get_root():
    return root


def load_or_create_salt():
    """Lädt Salt oder erstellt ein neues und speichert es ab."""
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        salt = cu.generate_salt()
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt


# Master-Passwort einmalig beim Start abfragen
if not os.path.exists(SALT_FILE):
    master_password = simpledialog.askstring(
        "Neues Master-Passwort",
        "Bitte ein neues Master-Passwort erstellen:",
        show="*"
    )
    if master_password is None:  # Cancel oder X
        root.destroy()
        sys.exit(0)
    if not master_password.strip():  # nur Enter/leer
        messagebox.showerror("Fehler", "Kein Master-Passwort eingegeben. Programm beendet.")
        root.destroy()
        sys.exit(0)

    salt = cu.generate_salt()
    with open(SALT_FILE, "wb") as f:
        f.write(salt)

else:
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
            key = cu.generate_key(master_password, salt)
            fernet = Fernet(key)

            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    daten = json.load(f)
                if daten:
                    cu.decrypt_text(daten[0]["Passwort"], fernet)  # Test-Decrypt

            break  # korrektes Passwort
        except Exception:
            messagebox.showerror("Fehler", "Falsches Master-Passwort!")


# HIER das Fenster sichtbar machen, nicht neu erstellen
root.deiconify()

listbox = tk.Listbox(root, width=50, height=10)

# Key initialisieren
key = cu.generate_key(master_password, salt)
fernet = Fernet(key)


def lade_listbox():
    """Lädt die gespeicherten Accounts aus der JSON-Datei in die Listbox."""
    listbox.delete(0, tk.END)

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            daten = json.load(f)
        except json.JSONDecodeError:
            daten = []

    for eintrag in daten:
        listbox.insert(tk.END, f"{eintrag['Account']} ({eintrag['Benutzername']})")


def passwort_hinzufuegen():
    """Fragt Account, Benutzername und Passwort ab und speichert sie verschlüsselt."""
    account = simpledialog.askstring("Account", "Account:")
    benutzername = simpledialog.askstring("Benutzername", "Benutzername:")
    passwort = simpledialog.askstring("Passwort", "Passwort:", show="*")

    if not account or not benutzername or not passwort:
        messagebox.showwarning("Fehler", "Alle Felder müssen ausgefüllt werden.")
        return

    verschluesselt = cu.encrypt_text(passwort, fernet)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                daten = json.load(f)
            except json.JSONDecodeError:
                daten = []
    else:
        daten = []

    daten.append({"Account": account, "Benutzername": benutzername, "Passwort": verschluesselt})

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=4)

    lade_listbox()
    messagebox.showinfo("Gespeichert", "Passwort wurde erfolgreich gespeichert.")


def get_passwort():
    """Zeigt das entschlüsselte Passwort für den ausgewählten Eintrag."""
    auswahl = listbox.curselection()
    if not auswahl:
        messagebox.showwarning("Fehler", "Bitte zuerst einen Eintrag auswählen.")
        return

    index = auswahl[0]

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        daten = json.load(f)

    eintrag = daten[index]
    entschluesselt = cu.decrypt_text(eintrag["Passwort"], fernet)

    messagebox.showinfo("Passwort", f"Account: {eintrag['Account']}\n"
                                    f"Benutzername: {eintrag['Benutzername']}\n"
                                    f"Passwort: {entschluesselt}")


def eintrag_löschen():
    """Löscht den ausgewählten Eintrag."""
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
    messagebox.showinfo("Gelöscht", f"Eintrag '{geloescht['Account']}' wurde gelöscht.")
