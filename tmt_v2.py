import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.okno = tk.Tk()
        self.okno.title("Task Management Tool - by Michal")

        self.entry = tk.Entry(self.okno, width=100)
        self.entry.pack(pady=10)

        self.przycisk_dodaj = tk.Button(self.okno, text="Dodaj zadanie", command=self.dodaj_zadanie, bg='#4CAF50', fg='white')
        self.przycisk_dodaj.pack(pady=5, fill='x')

        self.przycisk_usun = tk.Button(self.okno, text="Usuń zadanie", command=self.usun_zadanie, bg='#FF5733', fg='white')
        self.przycisk_usun.pack(pady=5, fill='x')

        self.przycisk_rozwinięcie = tk.Button(self.okno, text="Rozwiń zadanie", command=self.rozwinięcie_zadania, bg='#3498db', fg='white')
        self.przycisk_rozwinięcie.pack(pady=5, fill='x')

        self.przycisk_dodaj_osobe = tk.Button(self.okno, text="Dodaj osobę", command=self.dodaj_osobe, bg='#FF9800', fg='white')
        self.przycisk_dodaj_osobe.pack(pady=5, fill='x')

        self.przycisk_wyswietl_zadania = tk.Button(self.okno, text="Pokaż zadania osoby", command=self.wyswietl_zadania_osoby, bg='#8E44AD', fg='white')
        self.przycisk_wyswietl_zadania.pack(pady=5, fill='x')

        self.lista_box = tk.Listbox(self.okno, selectmode=tk.SINGLE, width=40, height=10)
        self.lista_box.pack(pady=10, fill='both', expand=True)
        self.lista_box.bind("<Double-Button-1>", self.podwójne_kliknięcie)

        self.zadania = []
        self.osoby = []

        self.wczytaj_z_pliku()  # Wczytaj dane z pliku podczas inicjalizacji

        self.aktualizuj_kolory_zadan()

    def dodaj_zadanie(self):
        zadanie_nazwa = self.entry.get()
        if zadanie_nazwa:
            if not self.osoby:
                messagebox.showwarning("Błąd", "Brak osób w systemie! Proszę dodać osobę najpierw.")
                return

            okno_przydzielenia = tk.Toplevel(self.okno)
            okno_przydzielenia.title("Przydziel zadanie do osoby")

            osoba_label = tk.Label(okno_przydzielenia, text="Wybierz osobę:")
            osoba_label.pack(pady=5)

            osoba_var = tk.StringVar(okno_przydzielenia)
            osoba_var.set(self.osoby[0])  # Domyślna wartość

            osoba_menu = tk.OptionMenu(okno_przydzielenia, osoba_var, *self.osoby)
            osoba_menu.pack(pady=5)

            def zapisz_przydzielenie():
                osoba = osoba_var.get()
                zadanie = {"nazwa": zadanie_nazwa, "status": "Nowy Status", "opis": "Nowy Opis", "osoba": osoba, "data": "Brak daty", "priorytet": "Brak priorytetu"}
                self.zadania.append(zadanie)
                self.lista_box.insert(tk.END, f"{zadanie_nazwa} (Przydzielone do: {osoba})")
                self.zapisz_do_pliku()
                self.aktualizuj_kolory_zadan()
                self.entry.delete(0, tk.END)  # Wyczyść pole po dodaniu zadania
                okno_przydzielenia.destroy()

            zapisz_button = tk.Button(okno_przydzielenia, text="Zapisz", command=zapisz_przydzielenie)
            zapisz_button.pack(pady=5)
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić nazwę zadania!")

    def usun_zadanie(self):
        try:
            wybrane_zadanie = self.lista_box.curselection()
            zadanie_index = wybrane_zadanie[0]
            self.lista_box.delete(wybrane_zadanie)
            del self.zadania[zadanie_index]
            self.zapisz_do_pliku()
            self.aktualizuj_kolory_zadan()
        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do usunięcia!")

    def rozwinięcie_zadania(self):
        try:
            wybrane_zadanie = self.lista_box.curselection()
            zadanie_index = wybrane_zadanie[0]
            zadanie_info = self.zadania[zadanie_index]

            okno_rozwinięcia = tk.Toplevel(self.okno)
            okno_rozwinięcia.title("Rozwinięcie zadania")

            status_label = tk.Label(okno_rozwinięcia, text="Status:")
            status_label.grid(row=0, column=0, padx=5, pady=5)
            status_entry = tk.Entry(okno_rozwinięcia)
            status_entry.grid(row=0, column=1, padx=5, pady=5)
            status_entry.insert(tk.END, zadanie_info["status"])

            opis_label = tk.Label(okno_rozwinięcia, text="Opis:")
            opis_label.grid(row=1, column=0, padx=5, pady=5)
            opis_entry = tk.Entry(okno_rozwinięcia)
            opis_entry.grid(row=1, column=1, padx=5, pady=5)
            opis_entry.insert(tk.END, zadanie_info["opis"])

            data_label = tk.Label(okno_rozwinięcia, text="Data wykonania:")
            data_label.grid(row=2, column=0, padx=5, pady=5)
            data_entry = tk.Entry(okno_rozwinięcia)
            data_entry.grid(row=2, column=1, padx=5, pady=5)
            data_entry.insert(tk.END, zadanie_info["data"])

            priorytet_label = tk.Label(okno_rozwinięcia, text="Priorytet:")
            priorytet_label.grid(row=3, column=0, padx=5, pady=5)
            priorytet_entry = ttk.Combobox(okno_rozwinięcia, values=list(range(1, 11)))
            priorytet_entry.grid(row=3, column=1, padx=5, pady=5)
            priorytet_entry.set(zadanie_info["priorytet"])

            osoba_label = tk.Label(okno_rozwinięcia, text="Osoba:")
            osoba_label.grid(row=4, column=0, padx=5, pady=5)
            osoba_info = tk.Label(okno_rozwinięcia, text=zadanie_info["osoba"])
            osoba_info.grid(row=4, column=1, padx=5, pady=5)

            zapisz_button = tk.Button(okno_rozwinięcia, text="Zapisz", command=lambda: self.zapisz_rozwinięcie(okno_rozwinięcia, zadanie_index, status_entry.get(), opis_entry.get(), data_entry.get(), priorytet_entry.get()))
            zapisz_button.grid(row=5, column=0, columnspan=2, pady=10)

            edytuj_button = tk.Button(okno_rozwinięcia, text="Edytuj", command=lambda: self.edytuj_zadanie(status_entry, opis_entry, data_entry, priorytet_entry, zadanie_index))
            edytuj_button.grid(row=6, column=0, columnspan=2, pady=5)

        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do rozwinięcia!")

    def edytuj_zadanie(self, status_entry, opis_entry, data_entry, priorytet_entry, indeks):
        status_entry.config(state=tk.NORMAL)
        opis_entry.config(state=tk.NORMAL)
        data_entry.config(state=tk.NORMAL)
        priorytet_entry.config(state=tk.NORMAL)
        status_entry.bind("<Return>", lambda event, i=indeks: self.zapisz_rozwinięcie(None, i, status_entry.get(), opis_entry.get(), data_entry.get(), priorytet_entry.get()))
        opis_entry.bind("<Return>", lambda event, i=indeks: self.zapisz_rozwinięcie(None, i, status_entry.get(), opis_entry.get(), data_entry.get(), priorytet_entry.get()))
        data_entry.bind("<Return>", lambda event, i=indeks: self.zapisz_rozwinięcie(None, i, status_entry.get(), opis_entry.get(), data_entry.get(), priorytet_entry.get()))
        priorytet_entry.bind("<Return>", lambda event, i=indeks: self.zapisz_rozwinięcie(None, i, status_entry.get(), opis_entry.get(), data_entry.get(), priorytet_entry.get()))

    def zapisz_rozwinięcie(self, okno_rozwinięcia, indeks, nowy_status, nowy_opis, nowa_data, nowy_priorytet):
        self.zadania[indeks]["status"] = nowy_status
        self.zadania[indeks]["opis"] = nowy_opis
        self.zadania[indeks]["data"] = nowa_data
        self.zadania[indeks]["priorytet"] = nowy_priorytet
        self.zapisz_do_pliku()
        self.aktualizuj_kolory_zadan()
        if okno_rozwinięcia:
            okno_rozwinięcia.destroy()

    def zapisz_do_pliku(self):
        with open("zadania.txt", "w") as plik:
            for zadanie in self.zadania:
                plik.write(f"{zadanie['nazwa']},{zadanie['status']},{zadanie['opis']},{zadanie['osoba']},{zadanie['data']},{zadanie['priorytet']}\n")
        with open("osoby.txt", "w") as plik:
            for osoba in self.osoby:
                plik.write(f"{osoba}\n")

    def wczytaj_z_pliku(self):
        self.zadania = []
        self.osoby = []
        try:
            with open("zadania.txt", "r") as plik:
                for linia in plik:
                    linia = linia.strip()
                    if linia:
                        zadanie_info = linia.split(",")
                        if len(zadanie_info) == 6:
                            zadanie = {"nazwa": zadanie_info[0], "status": zadanie_info[1], "opis": zadanie_info[2], "osoba": zadanie_info[3], "data": zadanie_info[4], "priorytet": zadanie_info[5]}
                            self.zadania.append(zadanie)
                            self.lista_box.insert(tk.END, f"{zadanie_info[0]} (Przydzielone do: {zadanie_info[3]})")
            with open("osoby.txt", "r") as plik:
                for linia in plik:
                    linia = linia.strip()
                    if linia:
                        self.osoby.append(linia)
        except FileNotFoundError:
            pass

    def aktualizuj_kolory_zadan(self):
        for i in range(self.lista_box.size()):
            if i % 2 == 0:
                self.lista_box.itemconfig(i, {'bg': '#D9D9D9'})  # Kolor dla parzystych zadań
            else:
                self.lista_box.itemconfig(i, {'bg': '#C0C0C0'})  # Kolor dla nieparzystych zadań

    def podwójne_kliknięcie(self, event):
        try:
            wybrane_zadanie = self.lista_box.curselection()
            zadanie_index = wybrane_zadanie[0]
            zadanie_info = self.zadania[zadanie_index]

            okno_rozwinięcia = tk.Toplevel(self.okno)
            okno_rozwinięcia.title("Rozwinięcie zadania")

            status_label = tk.Label(okno_rozwinięcia, text="Status:")
            status_label.grid(row=0, column=0, padx=5, pady=5)
            status_info = tk.Label(okno_rozwinięcia, text=zadanie_info["status"])
            status_info.grid(row=0, column=1, padx=5, pady=5)

            opis_label = tk.Label(okno_rozwinięcia, text="Opis:")
            opis_label.grid(row=1, column=0, padx=5, pady=5)
            opis_info = tk.Label(okno_rozwinięcia, text=zadanie_info["opis"])
            opis_info.grid(row=1, column=1, padx=5, pady=5)

            data_label = tk.Label(okno_rozwinięcia, text="Data wykonania:")
            data_label.grid(row=2, column=0, padx=5, pady=5)
            data_info = tk.Label(okno_rozwinięcia, text=zadanie_info["data"])
            data_info.grid(row=2, column=1, padx=5, pady=5)

            priorytet_label = tk.Label(okno_rozwinięcia, text="Priorytet:")
            priorytet_label.grid(row=3, column=0, padx=5, pady=5)
            priorytet_info = tk.Label(okno_rozwinięcia, text=zadanie_info["priorytet"])
            priorytet_info.grid(row=3, column=1, padx=5, pady=5)

            osoba_label = tk.Label(okno_rozwinięcia, text="Osoba:")
            osoba_label.grid(row=4, column=0, padx=5, pady=5)
            osoba_info = tk.Label(okno_rozwinięcia, text=zadanie_info["osoba"])
            osoba_info.grid(row=4, column=1, padx=5, pady=5)

        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do rozwinięcia!")

    def dodaj_osobe(self):
        okno_dodaj_osobe = tk.Toplevel(self.okno)
        okno_dodaj_osobe.title("Dodaj osobę")

        osoba_label = tk.Label(okno_dodaj_osobe, text="Nazwa osoby:")
        osoba_label.pack(pady=5)

        osoba_entry = tk.Entry(okno_dodaj_osobe)
        osoba_entry.pack(pady=5)

        def zapisz_osobe():
            osoba_nazwa = osoba_entry.get()
            if osoba_nazwa:
                self.osoby.append(osoba_nazwa)
                self.zapisz_do_pliku()
                okno_dodaj_osobe.destroy()
            else:
                messagebox.showwarning("Błąd", "Proszę wprowadzić nazwę osoby!")

        zapisz_button = tk.Button(okno_dodaj_osobe, text="Zapisz", command=zapisz_osobe)
        zapisz_button.pack(pady=5)

    def wyswietl_zadania_osoby(self):
        if not self.osoby:
            messagebox.showwarning("Błąd", "Brak osób w systemie!")
            return

        okno_wyswietl = tk.Toplevel(self.okno)
        okno_wyswietl.title("Zadania osoby")

        osoba_label = tk.Label(okno_wyswietl, text="Wybierz osobę:")
        osoba_label.pack(pady=5)

        osoba_var = tk.StringVar(okno_wyswietl)
        osoba_var.set(self.osoby[0])  # Domyślna wartość

        osoba_menu = tk.OptionMenu(okno_wyswietl, osoba_var, *self.osoby)
        osoba_menu.pack(pady=5)

        zadania_listbox = tk.Listbox(okno_wyswietl, width=40, height=10)
        zadania_listbox.pack(pady=10, fill='both', expand=True)

        def pokaz_zadania():
            zadania_listbox.delete(0, tk.END)
            osoba = osoba_var.get()
            for zadanie in self.zadania:
                if zadanie["osoba"] == osoba:
                    zadania_listbox.insert(tk.END, f"{zadanie['nazwa']} (Status: {zadanie['status']}, Opis: {zadanie['opis']}, Data: {zadanie['data']}, Priorytet: {zadanie['priorytet']})")

        pokaz_button = tk.Button(okno_wyswietl, text="Pokaż zadania", command=pokaz_zadania)
        pokaz_button.pack(pady=5)

    def uruchom(self):
        self.okno.mainloop()

manager_zadan = TaskManager()
manager_zadan.uruchom()
