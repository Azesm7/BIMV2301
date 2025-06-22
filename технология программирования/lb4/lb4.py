import tkinter as tk
from tkinter import messagebox

class MatrixAdderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сложение матриц A + B")
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.entries_a = []
        self.entries_b = []
        self.matrix_a_data = []
        self.n = 0
        self.m = 0

        self.setup_size_inputs()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def setup_size_inputs(self):
        self.entries_a.clear()
        self.entries_b.clear()
        self.matrix_a_data.clear()

        self.clear_frame()
        tk.Label(self.frame, text="Введите размерность матриц (NxM):").pack(pady=5)
        dim_frame = tk.Frame(self.frame)
        dim_frame.pack(pady=5)

        tk.Label(dim_frame, text="N:").grid(row=0, column=0)
        self.entry_n = tk.Entry(dim_frame, width=5)
        self.entry_n.grid(row=0, column=1)

        tk.Label(dim_frame, text="M:").grid(row=0, column=2)
        self.entry_m = tk.Entry(dim_frame, width=5)
        self.entry_m.grid(row=0, column=3)

        tk.Button(self.frame, text="Далее", command=self.handle_dimensions).pack(pady=10)

    def handle_dimensions(self):
        try:
            self.n = int(self.entry_n.get())
            self.m = int(self.entry_m.get())
            if not (1 <= self.n <= 10 and 1 <= self.m <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа от 1 до 10.")
            return

        self.setup_matrix_a()

    def setup_matrix_a(self):
        self.entries_a = []
        self.clear_frame()
        tk.Label(self.frame, text="Введите матрицу A").pack(pady=5)
        matrix_frame = tk.Frame(self.frame)
        matrix_frame.pack()

        for i in range(self.n):
            row = []
            for j in range(self.m):
                e = tk.Entry(matrix_frame, width=5)
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            self.entries_a.append(row)

        tk.Button(self.frame, text="← Назад", command=self.setup_size_inputs).pack(side="left", padx=5, pady=10)
        tk.Button(self.frame, text="Далее →", command=self.setup_matrix_b).pack(side="right", padx=5, pady=10)

    def setup_matrix_b(self):
        if not self.validate_entries(self.entries_a, "A"):
            return

        self.matrix_a_data = [[entry.get().strip() for entry in row] for row in self.entries_a]
        self.entries_b = []
        self.clear_frame()

        tk.Label(self.frame, text="Введите матрицу B").pack(pady=5)
        matrix_frame = tk.Frame(self.frame)
        matrix_frame.pack()

        for i in range(self.n):
            row = []
            for j in range(self.m):
                e = tk.Entry(matrix_frame, width=5)
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            self.entries_b.append(row)

        tk.Button(self.frame, text="← Назад", command=self.setup_matrix_a).pack(side="left", padx=5, pady=10)
        tk.Button(self.frame, text="Вычислить", command=self.calculate_sum).pack(side="right", padx=5, pady=10)

    def validate_entries(self, entries, name):
        for i, row in enumerate(entries):
            for j, e in enumerate(row):
                try:
                    int(e.get().strip())
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректное значение в матрице {name} ({i+1},{j+1})")
                    return False
        return True

    def calculate_sum(self):
        try:
            if not self.validate_entries(self.entries_b, "B"):
                return

            matrix_a = [[int(val) for val in row] for row in self.matrix_a_data]
            matrix_b = [[int(e.get().strip()) for e in row] for row in self.entries_b]
            result = [[matrix_a[i][j] + matrix_b[i][j] for j in range(self.m)] for i in range(self.n)]

            self.show_result(result)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить сложение:\n{e}")

    def show_result(self, result):
        self.clear_frame()
        tk.Label(self.frame, text="Результат C = A + B").pack(pady=5)
        result_frame = tk.Frame(self.frame)
        result_frame.pack()

        for i in range(self.n):
            for j in range(self.m):
                l = tk.Label(result_frame, text=str(result[i][j]), width=5, relief="ridge")
                l.grid(row=i, column=j, padx=2, pady=2)

        tk.Button(self.frame, text="← Назад", command=self.setup_matrix_b).pack(side="left", padx=5, pady=10)
        tk.Button(self.frame, text="Сбросить", command=self.setup_size_inputs).pack(side="right", padx=5, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixAdderApp(root)
    root.mainloop()
