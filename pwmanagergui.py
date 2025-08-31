import tkinter as tk
import pwmanager as pwm

# Holt das Hauptfenster aus dem pwmanager-Modul
root = pwm.get_root()
root.geometry("400x500")  # Setzt die Größe des Hauptfensters

# Label für den Titel der Anwendung
label = tk.Label(root, text="Passwort-Manager", font=("Arial", 16))
label.pack(pady=10)

# Button zum Hinzufügen eines neuen Passworts
btn_passwort_hinzufuegen = tk.Button(root, text="Neues Passwort hinzufügen", command=pwm.passwort_hinzufuegen, width=30, height=2)
btn_passwort_hinzufuegen.pack(pady=5)

# Button zum Abrufen eines Passworts
btn_passwort_holen = tk.Button(root, text="Passwort abrufen", command=pwm.get_passwort, width=30, height=2)
btn_passwort_holen.pack(pady=5)

# Button zum Löschen eines Eintrags
btn_passwort_holen = tk.Button(root, text="Eintrag löschen", command=pwm.eintrag_löschen, width=30, height=2)
btn_passwort_holen.pack(pady=5)

# Listbox aus dem pwmanager-Modul in das Hauptfenster einfügen
pwm.listbox.pack(padx=10, pady=10)

# Lädt die Listbox mit den gespeicherten Daten
pwm.lade_listbox()

# Startet die Hauptloop der Anwendung
root.mainloop()