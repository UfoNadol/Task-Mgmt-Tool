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

        self.przycisk_wyswietl_usuniete = tk.Button(self.okno, text="Pokaż usunięte zadania", command=self.wyswietl_usuniete_zadania, bg='#FF3333', fg='white')
        self.przycisk_wyswietl_usuniete.pack(pady=5, fill='x')

        self.lista_box = tk.Listbox(self.okno, selectmode=tk.SINGLE, width=40, height=10)
        self.lista_box.pack(pady=10, fill='both', expand=True)
        self.lista_box.bind("<Double-Button-1>", self.podwójne_kliknięcie)

        self.zadania = []
        self.usuniete_zadania = []
        self.osoby = []

        self.wczytaj_z_pliku()  # Wczytaj dane z pliku podczas inicjalizacji
        self.wczytaj_usuniete_z_pliku()

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
            zadanie_info = self.zadania[zadanie_index]

            # Dodaj zadanie do listy usuniętych zadań z datą usunięcia
            zadanie_info["data_usuniecia"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.usuniete_zadania.append(zadanie_info)
            self.zapisz_usuniete_do_pliku()

            self.lista_box.delete(wybrane_zadanie)
            del self.zadania[zadanie_index]
            self.zapisz_do_pliku()
            self.aktualizuj_kolory_zadan()
        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do usunięcia!")

    def przywroc_zadanie(self, zadanie_index):
        zadanie_info = self.usuniete_zadania[zadanie_index]

        # Przywróć zadanie do głównej listy
        del zadanie_info["data_usuniecia"]
        self.zadania.append(zadanie_info)

        self.usuniete_zadania.pop(zadanie_index)
        self.zapisz_usuniete_do_pliku()
        self.zapisz_do_pliku()

        self.lista_box.insert(tk.END, f"{zadanie_info['nazwa']} (Przydzielone do: {zadanie_info['osoba']})")
        self.aktualizuj_kolory_zadan()

    def wyswietl_usuniete_zadania(self):
        okno_usuniete = tk.Toplevel(self.okno)
        okno_usuniete.title("Usunięte zadania")

        usuniete_listbox = tk.Listbox(okno_usuniete, width=60, height=10)
        usuniete_listbox.pack(pady=10, fill='both', expand=True)

        for zadanie in self.usuniete_zadania:
            usuniete_listbox.insert(tk.END, f"{zadanie['nazwa']} (Osoba: {zadanie['osoba']}, Usunięte: {zadanie['data_usuniecia']})")

        def przywroc():
            try:
                wybrane_zadanie = usuniete_listbox.curselection()
                zadanie_index = wybrane_zadanie[0]
                self.przywroc_zadanie(zadanie_index)
                usuniete_listbox.delete(wybrane_zadanie)
            except IndexError:
                messagebox.showwarning("Błąd", "Proszę wybrać zadanie do przywrócenia!")

        przywroc_button = tk.Button(okno_usuniete, text="Przywróć zadanie", command=przywroc)
        przywroc_button.pack(pady=5)

    def zapisz_do_pliku(self):
        with open("zadania.txt", "w") as plik:
            for zadanie in self.zadania:
                plik.write(f"{zadanie['nazwa']},{zadanie['status']},{zadanie['opis']},{zadanie['osoba']},{zadanie['data']},{zadanie['priorytet']}\n")
        with open("osoby.txt", "w") as plik:
            for osoba in self.osoby:
                plik.write(f"{osoba}\n")

    def zapisz_usuniete_do_pliku(self):
        with open("usuniete_zadania.txt", "w") as plik:
            for zadanie in self.usuniete_zadania:
                plik.write(f"{zadanie['nazwa']},{zadanie['status']},{zadanie['opis']},{zadanie['osoba']},{zadanie['data']},{zadanie['priorytet']},{zadanie['data_usuniecia']}\n")

    def wczytaj_z_pliku(self):
        try:
            with open("zadania.txt", "r") as plik:
                for linia in plik:
                    zadanie_dane = linia.strip().split(",")
                    if len(zadanie_dane) == 6:
                        zadanie = {
                            "nazwa": zadanie_dane[0],
                            "status": zadanie_dane[1],
                            "opis": zadanie_dane[2],
                            "osoba": zadanie_dane[3],
                            "data": zadanie_dane[4],
                            "priorytet": zadanie_dane[5]
                        }
                        self.zadania.append(zadanie)
                        self.lista_box.insert(tk.END, f"{zadanie_dane[0]} (Przydzielone do: {zadanie_dane[3]})")
        except FileNotFoundError:
            pass

        try:
            with open("osoby.txt", "r") as plik:
                for linia in plik:
                    self.osoby.append(linia.strip())
        except FileNotFoundError:
            pass

    def wczytaj_usuniete_z_pliku(self):
        try:
            with open("usuniete_zadania.txt", "r") as plik:
                for linia in plik:
                    zadanie_dane = linia.strip().split(",")
                    if len(zadanie_dane) == 7:
                        zadanie = {
                            "nazwa": zadanie_dane[0],
                            "status": zadanie_dane[1],
                            "opis": zadanie_dane[2],
                            "osoba": zadanie_dane[3],
                            "data": zadanie_dane[4],
                            "priorytet": zadanie_dane[5],
                            "data_usuniecia": zadanie_dane[6]
                        }
                        self.usuniete_zadania.append(zadanie)
        except FileNotFoundError:
            pass

    def aktualizuj_kolory_zadan(self):
        self.lista_box.delete(0, tk.END)
        for zadanie in self.zadania:
            self.lista_box.insert(tk.END, f"{zadanie['nazwa']} (Przydzielone do: {zadanie['osoba']})")

    def podwójne_kliknięcie(self, event):
        try:
            wybrane_zadanie = self.lista_box.curselection()[0]
            zadanie = self.zadania[wybrane_zadanie]

            okno_zadania = tk.Toplevel(self.okno)
            okno_zadania.title("Szczegóły zadania")

            nazwa_label = tk.Label(okno_zadania, text=f"Nazwa: {zadanie['nazwa']}")
            nazwa_label.pack(pady=5)

            osoba_label = tk.Label(okno_zadania, text=f"Przydzielone do: {zadanie['osoba']}")
            osoba_label.pack(pady=5)

            status_label = tk.Label(okno_zadania, text=f"Status: {zadanie['status']}")
            status_label.pack(pady=5)

            opis_label = tk.Label(okno_zadania, text=f"Opis: {zadanie['opis']}")
            opis_label.pack(pady=5)

            data_label = tk.Label(okno_zadania, text=f"Data: {zadanie['data']}")
            data_label.pack(pady=5)

            priorytet_label = tk.Label(okno_zadania, text=f"Priorytet: {zadanie['priorytet']}")
            priorytet_label.pack(pady=5)

        except IndexError:
            pass

    def dodaj_osobe(self):
        osoba_nazwa = self.entry.get()
        if osoba_nazwa:
            self.osoby.append(osoba_nazwa)
            self.zapisz_do_pliku()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić nazwę osoby!")

    def wyswietl_zadania_osoby(self):
        osoba_nazwa = self.entry.get()
        if osoba_nazwa:
            zadania_osoby = [zadanie for zadanie in self.zadania if zadanie["osoba"] == osoba_nazwa]
            if zadania_osoby:
                okno_zadan_osoby = tk.Toplevel(self.okno)
                okno_zadan_osoby.title(f"Zadania przydzielone do: {osoba_nazwa}")

                lista_zadan_osoby = tk.Listbox(okno_zadan_osoby, width=60, height=10)
                lista_zadan_osoby.pack(pady=10)

                for zadanie in zadania_osoby:
                    lista_zadan_osoby.insert(tk.END, f"{zadanie['nazwa']} (Status: {zadanie['status']})")
            else:
                messagebox.showinfo("Brak zadań", f"Brak zadań przydzielonych do osoby {osoba_nazwa}.")
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić nazwę osoby!")

    def rozwinięcie_zadania(self):
        try:
            wybrane_zadanie = self.lista_box.curselection()
            zadanie_index = wybrane_zadanie[0]
            zadanie_info = self.zadania[zadanie_index]

            # Okno edycji zadania
            okno_rozwiniecie = tk.Toplevel(self.okno)
            okno_rozwiniecie.title(f"Edytuj zadanie: {zadanie_info['nazwa']}")

            status_label = tk.Label(okno_rozwiniecie, text="Status zadania:")
            status_label.pack(pady=5)

            status_entry = tk.Entry(okno_rozwiniecie)
            status_entry.insert(0, zadanie_info["status"])
            status_entry.pack(pady=5)

            opis_label = tk.Label(okno_rozwiniecie, text="Opis zadania:")
            opis_label.pack(pady=5)

            opis_entry = tk.Entry(okno_rozwiniecie)
            opis_entry.insert(0, zadanie_info["opis"])
            opis_entry.pack(pady=5)

            data_label = tk.Label(okno_rozwiniecie, text="Data zadania:")
            data_label.pack(pady=5)

            data_entry = tk.Entry(okno_rozwiniecie)
            data_entry.insert(0, zadanie_info["data"])
            data_entry.pack(pady=5)

            priorytet_label = tk.Label(okno_rozwiniecie, text="Priorytet zadania:")
            priorytet_label.pack(pady=5)

            priorytet_entry = tk.Entry(okno_rozwiniecie)
            priorytet_entry.insert(0, zadanie_info["priorytet"])
            priorytet_entry.pack(pady=5)

            def zapisz_edycje():
                zadanie_info["status"] = status_entry.get()
                zadanie_info["opis"] = opis_entry.get()
                zadanie_info["data"] = data_entry.get()
                zadanie_info["priorytet"] = priorytet_entry.get()
                self.zapisz_do_pliku()
                self.aktualizuj_kolory_zadan()
                okno_rozwiniecie.destroy()

            zapisz_button = tk.Button(okno_rozwiniecie, text="Zapisz zmiany", command=zapisz_edycje)
            zapisz_button.pack(pady=10)

        except IndexError:
            messagebox.showwarning("Błąd", "Proszę wybrać zadanie do edycji!")

if __name__ == "__main__":
    app = TaskManager()
    app.okno.mainloop()