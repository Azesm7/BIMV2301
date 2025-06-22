import tkinter as tk
from tkinter import messagebox

def sort_named_values():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        # Связь имя → значение
        variables = [("A", a), ("B", b), ("C", c)]

        # Сортировка по значению в убывающем порядке
        sorted_vars = sorted(variables, key=lambda x: x[1], reverse=True)

        # Формирование строки результата
        result = ", ".join([f"{name}={value}" for name, value in sorted_vars])
        label_result.config(text=result)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения.")

# Окно
root = tk.Tk()
root.title("Сортировка переменных по значению")

# Поля ввода
tk.Label(root, text="A:").grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="B:").grid(row=1, column=0, padx=5, pady=5)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="C:").grid(row=2, column=0, padx=5, pady=5)
entry_c = tk.Entry(root)
entry_c.grid(row=2, column=1, padx=5, pady=5)

# Кнопка сортировки
tk.Button(root, text="Сортировать", command=sort_named_values).grid(row=3, column=0, columnspan=2, pady=10)

# Вывод результата
label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
