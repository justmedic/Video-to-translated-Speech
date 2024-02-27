import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import sys

class Redirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Прокрутка к последней строке

    def flush(self):
        pass  

class TranslationApp:
    def __init__(self, root,callback):
        self.root = root
        self.root.title('VidTr v.0.1')
        root.resizable(False, False)
        
        # Поле ввода
        self.input_text = tk.Entry(root, width=100)
        self.input_text.pack(pady=10)
        
        # Список для голосов озвучки
        self.param1 = ttk.Combobox(root, values=['aidar', 'baya', 'kseniya', 'xenia', 'eugene'])
        self.param1.pack(pady=5)

        self.log = scrolledtext.ScrolledText(root, state='disabled', height=10)
        self.log.pack(pady=10)

        sys.stdout = Redirector(self.log)

        # Кнопка подтверждения
        self.confirm_button = tk.Button(root, text="Перевести", command=self.get_input)
        self.confirm_button.pack(pady=20)
        self.callback = callback

    # Функция, вызываемая при нажатии кнопки подтверждения
    def get_input(self):
        # Здесь можно добавить логику перевода
        url = self.input_text.get()
        voice_actor = self.param1.get()

        print(f"Введенный текст: {input}")
        print(f"Голос: {voice_actor}")

        self.callback(voice_actor, url)


