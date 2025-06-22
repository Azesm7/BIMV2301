import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "phonebook.json"

class PhonebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонный справочник")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f4f7")

        self.data = []
        self.load_data()

        self.create_widgets()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def create_widgets(self):
        # Поисковая панель с выбором поля
        search_frame = tk.Frame(self.root, bg="#f0f4f7")
        search_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(search_frame, text="Поиск по:", bg="#f0f4f7").pack(side=tk.LEFT, padx=(0,5))

        self.search_field = tk.StringVar(value="Фамилия")
        search_options = ["Фамилия", "Имя", "Отчество", "Телефон"]
        search_dropdown = ttk.Combobox(search_frame, textvariable=self.search_field, values=search_options, state="readonly", width=12)
        search_dropdown.pack(side=tk.LEFT)

        tk.Label(search_frame, text="Запрос:", bg="#f0f4f7").pack(side=tk.LEFT, padx=(10,5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))

        ttk.Button(search_frame, text="Найти", command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Сброс", command=self.reset_search).pack(side=tk.LEFT)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Фамилия", "Имя", "Отчество", "Телефон"), show="headings", selectmode="browse")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=170, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Кнопки действий
        btn_frame = tk.Frame(self.root, bg="#f0f4f7")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Добавить", command=self.add_entry).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Редактировать", command=self.edit_entry).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_entry).pack(side=tk.LEFT, padx=10)

        self.refresh_tree()

    def refresh_tree(self, items=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in (items if items is not None else self.data):
            if isinstance(entry, dict):
                self.tree.insert(
                    "", tk.END,
                    values=(
                        entry.get("Фамилия", ""),
                        entry.get("Имя", ""),
                        entry.get("Отчество", ""),
                        entry.get("Телефон", "")
                    )
                )

    def find_entry_by_values(self, values):
        values = [str(v).strip() for v in values]
        for entry in self.data:
            entry_values = [
                str(entry.get("Фамилия", "")).strip(),
                str(entry.get("Имя", "")).strip(),
                str(entry.get("Отчество", "")).strip(),
                str(entry.get("Телефон", "")).strip()
            ]
            if entry_values == values:
                return entry
        return None

    def search(self):
        field = self.search_field.get()
        query = self.search_var.get().strip().lower()
        if not query:
            self.refresh_tree()
            return
        results = []
        for entry in self.data:
            value = entry.get(field, "")
            if query in str(value).lower():
                results.append(entry)
        self.refresh_tree(results)

    def reset_search(self):
        self.search_var.set("")
        self.refresh_tree()

    def add_entry(self):
        self.open_form("Добавить абонента")

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите абонента для редактирования.")
            return
        values = self.tree.item(selected[0])["values"]
        entry = self.find_entry_by_values(values)
        if entry:
            self.open_form("Редактировать абонента", entry)
        else:
            messagebox.showerror("Ошибка", "Запись не найдена. Обновите таблицу.")

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите абонента для удаления.")
            return
        values = self.tree.item(selected[0])["values"]
        entry = self.find_entry_by_values(values)
        if entry:
            if messagebox.askyesno("Удалить", "Вы уверены, что хотите удалить запись?"):
                self.data.remove(entry)
                self.save_data()
                self.refresh_tree()
        else:
            messagebox.showerror("Ошибка", "Запись не найдена. Обновите таблицу.")

    def open_form(self, title, entry=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("400x300")
        form.configure(bg="#ffffff")
        form.resizable(False, False)
        form.grab_set()  # Модальное окно

        fields = ["Фамилия", "Имя", "Отчество", "Телефон"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(form, text=field, bg="#ffffff", anchor="w").grid(row=i, column=0, padx=15, pady=8, sticky="w")
            var = tk.StringVar(value=entry[field] if entry else "")
            e = ttk.Entry(form, textvariable=var)
            e.grid(row=i, column=1, padx=15, pady=8, sticky="ew")
            entries[field] = var

        form.columnconfigure(1, weight=1)

        def submit():
            new_data = {k: v.get().strip() for k, v in entries.items()}
            if not all(new_data.values()):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            if not new_data["Телефон"].isdigit():
                messagebox.showerror("Ошибка", "Телефон должен содержать только цифры.")
                return
            if entry:
                self.data.remove(entry)
            self.data.append(new_data)
            self.save_data()
            self.refresh_tree()
            form.destroy()

        ttk.Button(form, text="Сохранить", command=submit).grid(row=len(fields)+1, columnspan=2, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookApp(root)
    root.mainloop()
