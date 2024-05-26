import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.okno = tk.Tk()
        self.okno.title("Aplikacja To-Do List")

        self.notebook = ttk.Notebook(self.okno)
        self.notebook.pack(pady=10, expand=True)

        self.tab_zadania = ttk.Frame(self.notebook)
        self.tab_archiwum = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_zadania, text="Zadania")
        self.notebook.add(self.tab_archiwum, text="Archiwum")

        self.entry = tk.Entry(self.tab_zadania, width=40)
        self.entry.pack(pady=10)

        self.przycisk_dodaj = tk.Button(self.tab_zadania, text="Dodaj zadanie", command=self.dodaj_zadanie, bg='#4CAF50', fg='white')
        self.przycisk_dodaj.pack(pady=5, fill='x')

        self.przycisk_usun = tk.Button(self.tab_zadania, text="Usuń zadanie", command=self.usun_zadanie, bg='#FF5733', fg='white')
        self.przycisk_usun.pack(pady=5, fill='x')

        self.przycisk_rozwinięcie = tk.Button(self.tab_zadania, text="Rozwiń zadanie", command=self.rozwinięcie_zadania, bg='#3498db', fg='white')
        self.przycisk_rozwinięcie.pack(pady=5, fill='x')

        self.przycisk_edytuj_nazwe = tk.Button(self.tab_zadania, text="Edytuj nazwę zadania", command=self.edytuj_nazwe_zadania, bg='#FFA500', fg='white')
        self.przycisk_edytuj_nazwe.pack(pady=5, fill='x')

        self.lista_box = tk.Listbox(self.tab_zadania, selectmode=tk.SINGLE, width=40, height=10)
        self.lista_box.pack(pady=10, fill='both', expand=True)
        self.lista_box.bind("<Double-Button-1>", self.podwójne_kliknięcie)

        self.zadania = []
        self.archiwum = []

        self.kolumny = ("nazwa", "czas_usuniecia", "opis", "status")
        self.tabela_archiwum = ttk.Treeview(self.tab_archiwum, columns=self.kolumny, show="headings")
        for kolumna in self.kolumny:
            self.tabela_archiwum.heading(kolumna, text=kolumna.capitalize())
        self.tabela_archiwum.pack(fill='both', expand=True)

        self.przycisk_przywroc = tk.Button(self.tab_archiwum, text="Przywróć zadanie", command=self.przywroc_zadanie, bg='#4CAF50', fg='white')
        self.przycisk_przywroc.pack(pady=10)

        self.wczytaj_z_pliku()
        self.wczytaj_archiwum_z_pliku()

        self.aktualizuj_kolory_zadan()

    def dodaj_zadanie(self):
        zadanie_nazwa = self.entry.get()
        if zadanie_nazwa:
            zadanie = {"nazwa": zadanie_nazwa, "status": "Nowy Status", "opis": "Nowy Opis"}
            self.zadania.append(zadanie)
            self.lista_box.insert(tk.END, zadanie_nazwa)
            self.zapisz_do_pliku()
            self.aktualizuj_kolory_zadan()
            self.entry.delete(0, tk.END)  # Wyczyść pole po dodaniu zadania
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić nazwę zadania!")

    def usun_zadanie(self):
        try:
            wybrane_zadanie = self.lista_box.curselection()
            zadanie_index = wybrane_zadanie[0]
            zadanie_info = self.zadania[zadanie_index]
            czas_usuniecia = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            zadanie_archiwum = {
                "nazwa": zadanie_info["nazwa"],
                "czas_usuniecia": czas_usuniecia,
                "opis": zadanie_info["opis"],
                "status": zadanie_info["status"]
            }
            self.archiwum.append(zadanie_archiwum)
            self.tabela_archiwum.insert("", tk.END, values=(zadanie_archiwum["nazwa"], zadanie_archiwum["czas_usuniecia"], zadanie_archiwum["opis"], zadanie_archiwum["status"]))
            self.lista_box.delete(wybrane_zadanie)
            del self.zadania[zadanie_index]
            self.zapisz_do_pliku()
            self.zapisz_archiwum_do_pliku()
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

            zapisz_button = tk.Button(okno_rozwinięcia, text="Zapisz", command=lambda: self.zapisz_rozwinięcie(okno_rozwinięcia, zadanie_index, status_entry.get(), opis_entry.get()))
            zapisz_button.grid(row=2, column=0, columnspan=2, pady=10)

            edytuj_button = tk.Button(okno_rozwinięcia, text="Edytuj", command=lambda: self.edytuj_zadanie(status_entry, opis_entry, zadanie_index))
            edytuj_button.grid(row=3, column=0, columnspan=2, pady=5)

        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do rozwinięcia!")

    def edytuj_zadanie(self, status_entry, opis_entry, indeks):
        status_entry.config(state=tk.NORMAL)
        opis_entry.config(state=tk.NORMAL)
        status_entry.bind("<Return>", lambda event, i=indeks: self.zapisz_rozwinięcie(None, i, status_entry.get(), opis_entry.get()))
        opis_entry.bind("<Return>", lambda event, i=indeks: self.zapisz_rozwinięcie(None, i, status_entry.get(), opis_entry.get()))

    def zapisz_rozwinięcie(self, okno_rozwinięcia, indeks, nowy_status, nowy_opis):
        self.zadania[indeks]["status"] = nowy_status
        self.zadania[indeks]["opis"] = nowy_opis
        self.zapisz_do_pliku()
        self.aktualizuj_kolory_zadan()
        if okno_rozwinięcia:
            okno_rozwinięcia.destroy()

    def edytuj_nazwe_zadania(self):
        try:
            wybrane_zadanie = self.lista_box.curselection()
            zadanie_index = wybrane_zadanie[0]
            zadanie_info = self.zadania[zadanie_index]

            okno_edytowania = tk.Toplevel(self.okno)
            okno_edytowania.title("Edytuj nazwę zadania")

            nazwa_label = tk.Label(okno_edytowania, text="Nowa nazwa:")
            nazwa_label.grid(row=0, column=0, padx=5, pady=5)
            nazwa_entry = tk.Entry(okno_edytowania)
            nazwa_entry.grid(row=0, column=1, padx=5, pady=5)
            nazwa_entry.insert(tk.END, zadanie_info["nazwa"])

            zapisz_button = tk.Button(okno_edytowania, text="Zapisz", command=lambda: self.zapisz_nowa_nazwe(okno_edytowania, zadanie_index, nazwa_entry.get()))
            zapisz_button.grid(row=1, column=0, columnspan=2, pady=10)

        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do edytowania!")

    def zapisz_nowa_nazwe(self, okno_edytowania, indeks, nowa_nazwa):
        self.zadania[indeks]["nazwa"] = nowa_nazwa
        self.lista_box.delete(indeks)
        self.lista_box.insert(indeks, nowa_nazwa)
        self.zapisz_do_pliku()
        self.aktualizuj_kolory_zadan()
        okno_edytowania.destroy()

    def przywroc_zadanie(self):
        try:
            wybrane_zadanie = self.tabela_archiwum.selection()
            if not wybrane_zadanie:
                raise IndexError

            zadanie_values = self.tabela_archiwum.item(wybrane_zadanie, "values")
            zadanie_przywrocone = {
                "nazwa": zadanie_values[0],
                "status": zadanie_values[3],
                "opis": zadanie_values[2]
            }
            self.zadania.append(zadanie_przywrocone)
            self.lista_box.insert(tk.END, zadanie_przywrocone["nazwa"])
            self.zapisz_do_pliku()
            self.aktualizuj_kolory_zadan()
        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do przywrócenia!")

    def zapisz_do_pliku(self):
        with open("zadania.txt", "w") as plik:
            for zadanie in self.zadania:
                plik.write(f"{zadanie['nazwa']},{zadanie['status']},{zadanie['opis']}\n")

    def zapisz_archiwum_do_pliku(self):
        with open("archiwum.txt", "w") as plik:
            for zadanie in self.archiwum:
                plik.write(f"{zadanie['nazwa']},{zadanie['czas_usuniecia']},{zadanie['opis']},{zadanie['status']}\n")

    def wczytaj_z_pliku(self):
        self.zadania = []
        try:
            with open("zadania.txt", "r") as plik:
                for linia in plik:
                    linia = linia.strip()
                    if linia:
                        zadanie_info = linia.split(",")
                        if len(zadanie_info) == 3:
                            zadanie = {"nazwa": zadanie_info[0], "status": zadanie_info[1], "opis": zadanie_info[2]}
                            self.zadania.append(zadanie)
                            self.lista_box.insert(tk.END, zadanie_info[0])
        except FileNotFoundError:
            pass

    def wczytaj_archiwum_z_pliku(self):
        self.archiwum = []
        try:
            with open("archiwum.txt", "r") as plik:
                for linia in plik:
                    linia = linia.strip()
                    if linia:
                        zadanie_info = linia.split(",")
                        if len(zadanie_info) == 4:
                            zadanie_archiwum = {"nazwa": zadanie_info[0], "czas_usuniecia": zadanie_info[1], "opis": zadanie_info[2], "status": zadanie_info[3]}
                            self.archiwum.append(zadanie_archiwum)
                            self.tabela_archiwum.insert("", tk.END, values=(zadanie_archiwum["nazwa"], zadanie_archiwum["czas_usuniecia"], zadanie_archiwum["opis"], zadanie_archiwum["status"]))
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

        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do rozwinięcia!")

    def uruchom(self):
        self.okno.mainloop()

manager_zadan = TaskManager()
manager_zadan.uruchom()
