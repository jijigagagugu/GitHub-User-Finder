import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

# путь к файлу избранных пользователей
FAVORITES_FILE = 'favorites.json'

# инициализация файла избранных
if not os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump([], f)

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title('GitHub User Finder')
        self.favorites = self.load_favorites()

        # Поле поиска
        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.pack(pady=10)

        # Кнопка поиска
        self.search_button = tk.Button(root, text='Поиск пользователя', command=self.search_user)
        self.search_button.pack()

        # Список результатов
        self.results_listbox = tk.Listbox(root, width=50, height=10)
        self.results_listbox.pack(pady=10)

        # Кнопки для добавления в избранное
        self.add_fav_button = tk.Button(root, text='Добавить в избранное', command=self.add_to_favorites)
        self.add_fav_button.pack(pady=5)

        # Список избранных пользователей
        self.favorites_label = tk.Label(root, text='Избранные пользователь:')
        self.favorites_label.pack()

        self.favorites_listbox = tk.Listbox(root, width=50, height=10)
        self.favorites_listbox.pack(pady=10)
        self.update_favorites_listbox()

    def load_favorites(self):
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)

    def save_favorites(self):
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(self.favorites, f, indent=4)

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror('Ошибка', 'Поле поиска не должно быть пустым.')
            return
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            display_text = f"{user_data.get('login')} - {user_data.get('name') or 'Нет имени'}"
            # Очистка списка и добавление результата
            self.results_listbox.delete(0, tk.END)
            self.results_listbox.insert(tk.END, display_text)
            # Сохраняем данные пользователя для добавления в избранное
            self.current_user = user_data
        else:
            messagebox.showerror('Ошибка', 'Пользователь не найден.')
            self.results_listbox.delete(0, tk.END)

    def add_to_favorites(self):
        if hasattr(self, 'current_user'):
            login = self.current_user.get('login')
            if login in [user['login'] for user in self.favorites]:
                messagebox.showinfo('Информация', 'Этот пользователь уже в избранных.')
            else:
                self.favorites.append(self.current_user)
                self.save_favorites()
                self.update_favorites_listbox()
                messagebox.showinfo('Успех', 'Пользователь добавлен в избранное.')
        else:
            messagebox.showerror('Ошибка', 'Сначала выполните поиск пользователя.')

    def update_favorites_listbox(self):
        self.favorites_listbox.delete(0, tk.END)
        for user in self.favorites:
            display_text = f"{user.get('login')} - {user.get('name') or 'Нет имени'}"
            self.favorites_listbox.insert(tk.END, display_text)

if __name__ == '__main__':
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
