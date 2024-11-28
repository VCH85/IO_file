from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk
import requests
import pyperclip
import json
import os

history_file = "upload-history.json"


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    history.append({"file_path": os.path.basename(file_path), "download_link": download_link})
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)
def upload():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath) as f:
                files = {"file": f}
                response = requests.post("https://file.io", files = files)
                response.raise_for_status()
                download_link = response.json().get("link")
                entry.delete(0, END)
                entry.insert(0,download_link)
                pyperclip.copy(download_link)
                save_history(filepath, download_link)
                mb.showinfo("Загрузка файла", "Ссылка скопирована в буфер обмена")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")


def show_history():
    if not os.path.exists(history_file):
        mb.showinfo("", "история загрузок пуста")
        return

    history_window = Toplevel(window)
    history_window.title("История загрузок")
    file_listbox = Listbox(history_window, width=50, height=20)
    file_listbox.grid(row=0, column=0, padx=(10,0), pady=10)
    links_listbox = Listbox(history_window, width = 50, height=20)
    links_listbox.grid(row=0, column=1, padx=(0,10), pady=10)

    with open(history_file, 'r') as f:
        history = json.load(f)
        for item in history:
            file_listbox.insert(END, item["file_path"])
            links_listbox.insert(END, item["download_link"])


window = Tk()
window.title("Сохранение файла в облаке")
window.geometry("400x200")

button = ttk.Button(text="Загрузить файл", command= upload)
button.pack()

entry = ttk.Entry()
entry.pack()

button_history = ttk.Button(text="История запросов", command= show_history)
button_history.pack()

window.mainloop()


