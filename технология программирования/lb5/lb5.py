import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class SalesPieChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ продаж")
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.entries = []
        self.n = 0

        self.setup_n_input()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def setup_n_input(self):
        self.clear_frame()
        tk.Label(self.frame, text="Введите количество видов товаров (1–10):").pack(pady=5)
        self.entry_n = tk.Entry(self.frame, width=5)
        self.entry_n.pack(pady=5)
        tk.Button(self.frame, text="Далее", command=self.handle_n).pack(pady=10)

    def handle_n(self):
        try:
            self.n = int(self.entry_n.get())
            if not (1 <= self.n <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число от 1 до 10.")
            return

        self.setup_sales_inputs()

    def setup_sales_inputs(self):
        self.clear_frame()
        tk.Label(self.frame, text="Введите данные о товарах:").pack(pady=5)

        sales_frame = tk.Frame(self.frame)
        sales_frame.pack()

        headers = ["Название", "Цена", "Количество"]
        for j, header in enumerate(headers):
            tk.Label(sales_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=j, padx=5, pady=5)

        self.entries = []
        for i in range(self.n):
            row = []
            for j in range(3):
                e = tk.Entry(sales_frame, width=15)
                e.grid(row=i+1, column=j, padx=5, pady=5)
                row.append(e)
            self.entries.append(row)

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="← Назад", command=self.setup_n_input).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Построить диаграмму", command=self.build_pie_chart).pack(side="right", padx=5)

    def build_pie_chart(self):
        try:
            names = []
            totals = []
            for i, row in enumerate(self.entries):
                name = row[0].get().strip()
                price = float(row[1].get())
                qty = float(row[2].get())

                if not name:
                    raise ValueError(f"Не указано название товара в строке {i + 1}")
                if price < 0 or qty < 0:
                    raise ValueError(f"Цена и количество не могут быть отрицательными (строка {i + 1})")

                total = price * qty
                names.append(name)
                totals.append(total)

            self.show_pie_chart(names, totals)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка ввода: {e}")

    def show_pie_chart(self, names, totals):
        self.clear_frame()
        tk.Label(self.frame, text="Процентные доли стоимости продаж").pack(pady=5)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(totals, labels=names, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        tk.Button(self.frame, text="← Назад", command=self.setup_sales_inputs).pack(pady=10)


root = tk.Tk()
app = SalesPieChartApp(root)
root.mainloop()

