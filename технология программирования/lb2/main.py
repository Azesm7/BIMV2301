import tkinter as tk
from tkinter import messagebox
import math

def solve_quadratic():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        if a == 0:
            messagebox.showerror("Ошибка", "Коэффициент A не должен быть равен 0.")
            return

        discriminant = b ** 2 - 4 * a * c

        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            result = f"Два корня:\nX₁ = {x1:.4f}\nX₂ = {x2:.4f}"
        elif discriminant == 0:
            x = -b / (2 * a)
            result = f"Один корень:\nX = {x:.4f}"
        else:
            result = "Действительных корней нет."

        label_result.config(text=result)

    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовые значения.")

# Создание окна
root = tk.Tk()
root.title("Квадратное уравнение")

# Поля для ввода коэффициентов
tk.Label(root, text="A:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="B:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="C:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_c = tk.Entry(root)
entry_c.grid(row=2, column=1, padx=5, pady=5)

# Кнопка решения
tk.Button(root, text="Решить", command=solve_quadratic).grid(row=3, column=0, columnspan=2, pady=10)

# Метка для вывода результата
label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
