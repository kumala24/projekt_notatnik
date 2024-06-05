from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os.path
import ttkbootstrap as tb


# tworzenie klasy Notepad
class Notepad(tk.Tk):

    # funkcja do tworzenia instancji klasy
    def __init__(self):
        self.root = tk.Tk()  # Tworzenie okna
        self.root.title("Notatnik")  # Dodawanie tytułu
        self.root.minsize(800, 400)  # Minimalny rozmiar okna
        self.root.resizable(True, True)  # możliwość rozciągania okna

        # tworzenie pola tekstowego
        self.textbox = tk.Text(self.root, height='2', font=('Arial', 15), selectbackground='gray') # przechwytywanie, zastosowac, dodanie pola tekstowego do okna
        self.textbox.bind()
        self.textbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)  # pole tekstowe dopasowanie do rozmiaru okna

        # dodanie belki przewijania z prawej strony
        self.y_scrollbar = tb.Scrollbar(self.textbox, orient='vertical', command=self.textbox.yview)  # komenda przesuń
        self.textbox.config(yscrollcommand=self.y_scrollbar.set)  # komenda przesuń
        self.y_scrollbar.pack(side='right', fill='y')  # dołączenie belki, umieszczenie jej z prawej i wypełnienie w 'y'

        # tworzenie menu "Plik" rozwijanego kaskadowo z 4 zakładkami
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Nowy plik', command=self.new_file)  # dodanie zakładki
        self.filemenu.add_command(label='Nowy plik w nowym oknie', command=self.__init__)
        self.filemenu.add_command(label='Zapisz jako', command=self.save_as)  # dodanie zakładki 'zapisz jako'
        self.filemenu.add_command(label='Otwórz', command=self.open_txt)
        self.filemenu.add_separator()  # dodanie separatora
        self.filemenu.add_command(label='Zamknij', command=self.close)
        self.menubar.add_cascade(menu=self.filemenu, label='Plik')  # wrzucenie rozwijanego menu do okna

        # dodanie zakładki do ustawienia czcionki
        self.menubar.add_command(label='Ustawienia czcionki', command=self.font)

        # tworzenie kolejnego menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)  # tworzenie menu głównego
        self.filemenu.add_command(label='Wielkie litery', command=self.upper)  # dodanie zakładki 'zapisz jako'
        self.filemenu.add_command(label='Małe litery', command=self.lower)
        self.filemenu.add_command(label='Kopiuj', command=self.copy_text)
        self.filemenu.add_command(label='Wklej', command=self.paste_text)
        self.filemenu.add_command(label='Wytnij', command=self.cut_text)
        self.menubar.add_cascade(menu=self.filemenu, label='Edytuj')  # stworzenie rozwijanego menu o nazwie plik

        self.menubar.add_command(label='Wyczyść wszystko', command=self.clearall)  # Dodanie przycisku do czyszczenia pola tekstowego
        self.menubar.add_command(label='Wyczyść zaznaczone', command=self.clear)
        self.menubar.add_command(label='Zakreśl', command=self.mark)

        self.root.config(menu=self.menubar)  # wrzucenie paska z wszystkimi zakładkami do okna

        self.root.mainloop()  # uruchomienie

    # metoda tworzenia nowego pliku
    def new_file(self):
        #if self.textbox.get(1.0, tk.END) != 0:
        if messagebox.askyesno(title="Notatnik", message='Dotychczasowa praca mogła niezostać zapisana, czy chcesz ją zapisać?'):  # zapytanie
            self.save_as()  # wywołanie metody zapisz
            self.clearall()  # wywołanie metody wyczyść
        else:
            self.clearall()
            self.root.title('Nowy plik')  # ustawienie tytułu nowego pliku jako nowy plik

    # metoda zapisu
    def save_as(self):
        text_file = filedialog.asksaveasfilename(defaultextension='.*', initialdir=r'C:\\Users\\kumala\\', title="Zapisz jako", filetypes=(("Plik tekstowy (txt)", "*.txt"), ("Plik tekstowy (doc)", "*.doc"), ("Plik PDF", ("*.pdf"))))
        if text_file:
            self.root.title(f'{text_file} Notatnik')
            text_file = open(text_file, 'w')  # otwieranie pliku w trybie zapisu
            text_file.write(self.textbox.get(1.0, tk.END))  # zapisywanie każdego elementu z pola tekstowego
            text_file.close()  # zamykanie pliku

    # metoda otwierania istniejącego pliku
    def open_txt(self):
        text_file = self.file = askopenfilename(defaultextension=".txt", filetypes=[('Wszystkie pliki', "*.*"), ("Pliki tekstowe", '*.txt')])
        if text_file == "":
            text_file = None
        else:
            self.root.title(os.path.basename(text_file))  # dodanie tytułu na belce
            self.clearall()  # wyczyszcenie pola tekstowego
            text_file = open(text_file, "r")  # otwarcie pliku w trybie odczytu
            ridding = text_file.read()  # przypisanie do zmiennej otwartego pliku
            self.textbox.insert(tk.END, ridding)
            text_file.close()  # zamknięcie otwartego pliku

    # zmiana ustawień czcionki
    def font(self):
        self.top = tk.Toplevel()  # tworzenie drugiego okna klasy toplevel
        self.top.title("Ustawienia czcionki")
        self.top.geometry('400x400')
        self.top.resizable(False, False)  # okno nie jest rozciągalne

        self.zakladka = ttk.Notebook(self.top)  # notebook widget

        # tworzenie ramki
        self.frame = ttk.Frame(self.zakladka)  # tworzenie ramki
        self.frame2 = ttk.Frame(self.zakladka)

        self.zakladka.add(self.frame, text='wielkość czcionki')  # dodanie zakładki ustawienia wielkości czcionki

        self.label = tk.Label(self.frame, text='Wpisz wielkość czcionki')  # tworzenie labelki
        self.label.pack(fill='x')  # dodanie labelki do okna

        self.entry = tk.Entry(self.frame)  # utworzenie pola tekstowego
        self.entry.pack(fill='x', padx=10, pady=10)

        self.zakladka.add(self.frame2, text='rodzaj')  # tworzenie zakładki w ktorej mozna ustawic rodzaj czcionki

        # current_var = self.combobox.get()
        # combobox z rodzajami czcionek
        self.combobox = ttk.Combobox(self.frame2, values=['Arial', 'Arial Black', 'Calibri', 'Corbel', 'Forte', 'Georgia', 'Impact', 'Magneto', 'Perpetua', 'Selawik', 'Times New Roman', 'Wide Latin'])
        self.combobox.pack(padx=10, pady=10)

        self.label2 = tk.Label(self.frame2, text='Wybierz czcionke', )  # tworzenie labelki
        self.label2.pack(fill='x', padx=10, pady=10)

        self.label2 = tk.Label(self.frame, text="""Aby potwierdzić przejdź do następnej karty 
        i wcisnij 'Potwierdź'. Pamiętaj, aby za każdym razem 
        wpisać wielkość czionki.""", justify='center')  # tworzenie labelki
        self.label2.pack(fill='x', padx=10, pady=10, side='bottom')

        self.button = tk.Button(self.frame2, text='Potwierdź', command=self.topButton)  # dodanie przycisku potwierdź
        self.button.pack(side='bottom', padx=20, pady=40)  # umiejscowienie przycisku na dole okna, z marginesami

        self.zakladka.pack(expand=1, fill='both')

    # tworzenie metody uppercase do powięszania wszystkich liter
    def upper(self):
        if self.textbox.selection_get():  # sprawdzanie zaznaczenia
            strings = self.textbox.selection_get()  # przypisanie zaznaczenia do zmiennej
            upper_strings = strings.upper()  # wykonanie upper
            self.textbox.replace('sel.first', 'sel.last', upper_strings)  # podmianka

    # metoda lowercase do pomniejszania wszystkich liter
    def lower(self):
        if self.textbox.selection_get():  # sprawdzanie zaznaczenia
            strings = self.textbox.selection_get()  # przypisanie zaznaczenia do zmiennej
            upper_strings = strings.lower()  # wykonanie lower
            self.textbox.replace('sel.first', 'sel.last', upper_strings)

    # metoda do kopiowania zawartości pola tekstowego
    def copy_text(self):
        self.textbox.event_generate("<<Copy>>")  # metoda kopiowania
        messagebox.showinfo(title="Notatnik", message='Tekst został przeniesiony do schowka.')  # wyświetlenie komunikatu

    # metoda do wklejania skopiowanego elementu
    def paste_text(self):
        self.textbox.event_generate("<<Paste>>")  # wykonanie metody wklej

    # wycinanie
    def cut_text(self):
        self.textbox.event_generate("<<Cut>>")  # wykonanie metody wytnij

    # zamykanie
    def close(self):
        if messagebox.askyesno(title="Notatnik", message='Dotychczasowa praca nie została zapisana, czy chcesz ją zapisać?'):  # dodanie wiadomości z zapytaniem
            self.save_as()  # wywołanie metody zapisz
            self.root.destroy()  # zamknięcie
        else:
            self.root.destroy()

    # metoda do czyszczenia pola tekstowego
    def clearall(self):
        self.textbox.delete('1.0', tk.END)  # wyczyść pole tekstowe

    # czyszczenie zaznaczonego fragmentu
    def clear(self):
        if self.textbox.selection_get():
            #selected = self.textbox.selection_get()
            self.textbox.delete('sel.first', 'sel.last')

    # zakreślanie zaznaczonego pola
    def mark(self):
        if self.textbox.selection_get():
            selected = self.textbox.selection_get()
            self.textbox.tag_config('tag', background='yellow')  # dodanie znacznika
            self.textbox.insert('sel.first', selected, 'tag')  # wstawienie do textboxa na indeks sel.first tagu ze zmodulowanym bg
            self.textbox.delete('sel.first', 'sel.last')  # usuniecie wybranego przedziału znaków

    # przycisk do okna klasyu toplewel wprowadzający zamiany czcionki
    def topButton(self):
        type = self.combobox.get()  # pobranie czcionki
        size = self.entry.get()  # pobranie wartości z pola entry i zapisanie pod zmienną size
        msg = f'wybrałeś rozmiar czcionki: {self.entry.get()}, i typ: {type}'  # wiadomość o wybraniu opcji czcionki
        messagebox.showinfo(title='Info', message=msg)  # utworzenie wiadomości o tytule info, i tresci message

        self.textbox.configure(font=(f'{type}', f'{size}'))  # edycja tekstu
        self.textbox.bind()
        self.top.destroy()  # zamknięcie okna


Notepad()  # uruchomienie klasy
