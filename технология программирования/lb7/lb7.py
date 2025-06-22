import tkinter as tk
from tkinter import ttk, messagebox


class EnhancedTaskSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Решатель задач (интерактивно)")
        self.root.geometry("650x500")

        self.precision = 4
        self.task_var = tk.IntVar(value=0)
        self.input_var = tk.StringVar()
        self.operation_var = tk.StringVar()
        self.step = 0
        self.inputs = []
        self.results_history = []
        self.current_task = None

        self.build_ui()

    def build_ui(self):
        tasks_frame = ttk.LabelFrame(self.root, text="Выберите задачу")
        tasks_frame.pack(padx=10, pady=10, fill="x")

        tasks = [
            ("1. Найти гипотенузу C треугольника (A, B)", 1),
            ("2. Найти скорость V и путь S (V0, a, t)", 2),
            ("3. Вычислить Y = A+B, A/B, A*B (выбор операции)", 3),
            ("4. Вычислить X=A+B, Y=A/B, Z=A*B", 4),
        ]
        for text, val in tasks:
            rb = ttk.Radiobutton(tasks_frame, text=text, variable=self.task_var, value=val, command=self.start_task)
            rb.pack(anchor="w", padx=5, pady=2)

        self.info_label = ttk.Label(self.root, text="Выберите задачу")
        self.info_label.pack(padx=10, pady=5)

        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(padx=10, pady=5, fill="x")

        self.input_entry = ttk.Entry(entry_frame, textvariable=self.input_var, font=("Consolas", 14))
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<KeyRelease>", self.on_input_change)

        self.next_button = ttk.Button(entry_frame, text="Следующий", command=self.on_next, state="disabled")
        self.next_button.pack(side="left", padx=5)

        self.reset_button = ttk.Button(entry_frame, text="Очистить", command=self.reset_all, state="disabled")
        self.reset_button.pack(side="left")

        self.error_label = ttk.Label(self.root, text="", foreground="red")
        self.error_label.pack(padx=10, pady=2)

        op_frame = ttk.Frame(self.root)
        op_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(op_frame, text="Выберите операцию:").pack(side="left")

        self.operation_combo = ttk.Combobox(op_frame, textvariable=self.operation_var, values=["+", "/", "*"], state="readonly")
        self.operation_combo.pack(side="left", padx=5)
        self.operation_combo.bind("<<ComboboxSelected>>", self.on_operation_selected)
        self.operation_combo.pack_forget()

        results_frame = ttk.LabelFrame(self.root, text="Результаты")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.result_text = tk.Text(results_frame, height=12, font=("Consolas", 11), state="disabled")
        self.result_text.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.show_all_btn = ttk.Button(btn_frame, text="Показать решения", command=self.show_all_solutions)
        self.show_all_btn.pack()

    def start_task(self):
        self.reset_all()
        task = self.task_var.get()
        self.current_task = task
        self.inputs = []
        self.step = 0
        self.error_label.config(text="")
        self.operation_var.set("")
        self.operation_combo.pack_forget()
        self.next_button.config(state="disabled")
        self.input_entry.config(state="normal")
        self.input_var.set("")

        if task == 1:
            self.info_label.config(text="Введите катет A (число):")
        elif task == 2:
            self.info_label.config(text="Введите начальную скорость V0 (число):")
        elif task == 3:
            self.info_label.config(text="Введите число A:")
        elif task == 4:
            self.info_label.config(text="Введите число A:")

    def on_input_change(self, event=None):
        text = self.input_var.get().strip()
        if self.current_task in [1, 2, 4]:
            self.next_button.config(state="normal" if text else "disabled")
        elif self.current_task == 3:
            if self.step in [0, 1]:
                self.next_button.config(state="normal" if text else "disabled")
            elif self.step == 2:
                self.next_button.config(state="disabled")
        self.error_label.config(text="")

    def on_operation_selected(self, event):
        if self.operation_var.get() in ["+", "/", "*"]:
            self.next_button.config(state="normal")
            self.error_label.config(text="")
        else:
            self.next_button.config(state="disabled")

    def solve_task_3_operation(self, operation):
        A, B = self.inputs
        if operation == "+":
            Y = A + B
            text = f"Y = A + B = {A} + {B} = {Y:.{self.precision}f}"
        elif operation == "/":
            if B == 0:
                self.error_label.config(text="Деление на ноль невозможно.")
                return
            Y = A / B
            text = f"Y = A / B = {A} / {B} = {Y:.{self.precision}f}"
        elif operation == "*":
            Y = A * B
            text = f"Y = A * B = {A} * {B} = {Y:.{self.precision}f}"
        else:
            self.error_label.config(text="Неизвестная операция")
            return
        self.show_result(text)

    def on_next(self):
        # Особая обработка для задачи 3, шаг 2 — выбор операции
        if self.current_task == 3 and self.step == 2:
            operation = self.operation_var.get()
            if operation not in ["+", "/", "*"]:
                self.error_label.config(text="Выберите операцию из списка")
                return
            self.solve_task_3_operation(operation)
            return

        val = self.input_var.get().strip()
        if self.current_task is None or self.current_task == 0:
            self.error_label.config(text="Выберите задачу")
            return

        # Проверяем ввод числа, если нужно
        if self.current_task != 3 or (self.current_task == 3 and self.step in [0, 1]):
            try:
                num = float(val)
            except ValueError:
                self.error_label.config(text="Введите корректное число")
                return
            self.inputs.append(num)
            self.input_var.set("")
            self.step += 1

        # Логика по шагам
        if self.current_task == 1:
            if self.step == 1:
                self.info_label.config(text="Введите катет B (число):")
                self.next_button.config(state="disabled")
            elif self.step == 2:
                A, B = self.inputs
                C = (A**2 + B**2) ** 0.5
                text = f"Гипотенуза C = sqrt({A}² + {B}²) = {C:.{self.precision}f}"
                self.show_result(text)

        elif self.current_task == 2:
            prompts = ["Введите ускорение a (число):", "Введите время t (число):"]
            if self.step < 3:
                self.info_label.config(text=prompts[self.step-1])
                self.next_button.config(state="disabled")
            elif self.step == 3:
                V0, a, t = self.inputs
                V = V0 + a * t
                S = V0 * t + 0.5 * a * t**2
                text = (
                    f"Скорость V = V0 + a*t = {V0} + {a}*{t} = {V:.{self.precision}f}\n"
                    f"Пройденное расстояние S = V0*t + 0.5*a*t² = {S:.{self.precision}f}"
                )
                self.show_result(text)

        elif self.current_task == 3:
            if self.step == 1:
                self.info_label.config(text="Введите число B:")
                self.next_button.config(state="disabled")
            elif self.step == 2:
                self.info_label.config(text="Выберите операцию:")
                self.input_entry.config(state="disabled")
                self.operation_combo.pack(side="left", padx=5)
                self.next_button.config(state="disabled")

        elif self.current_task == 4:
            if self.step == 1:
                self.info_label.config(text="Введите число B:")
                self.next_button.config(state="disabled")
            elif self.step == 2:
                A, B = self.inputs
                if B == 0:
                    self.error_label.config(text="Деление на ноль невозможно.")
                    return
                X = A + B
                Y = A / B
                Z = A * B
                text = (
                    f"X = A + B = {A:.{self.precision}f} + {B:.{self.precision}f} = {X:.{self.precision}f}\n"
                    f"Y = A / B = {A:.{self.precision}f} / {B:.{self.precision}f} = {Y:.{self.precision}f}\n"
                    f"Z = A * B = {A:.{self.precision}f} * {B:.{self.precision}f} = {Z:.{self.precision}f}"
                )
                self.show_result(text)

    def show_result(self, text):
        self.results_history.append(text)
        self.result_text.config(state="normal")
        self.result_text.insert("end", text + "\n\n")
        self.result_text.see("end")
        self.result_text.config(state="disabled")
        self.error_label.config(text="")
        self.info_label.config(text="Результат получен. Выберите задачу для новой работы.")
        self.next_button.config(state="disabled")
        self.input_entry.config(state="disabled")
        self.operation_combo.pack_forget()
        self.reset_button.config(state="normal")
        self.step = 0
        self.inputs = []
        self.current_task = None
        self.task_var.set(0)

    def reset_all(self):
        self.step = 0
        self.inputs = []
        self.input_var.set("")
        self.operation_var.set("")
        self.error_label.config(text="")
        self.info_label.config(text="Выберите задачу")
        self.next_button.config(state="disabled")
        self.input_entry.config(state="normal")
        self.operation_combo.pack_forget()
        self.reset_button.config(state="disabled")

    def show_all_solutions(self):
        if not self.results_history:
            messagebox.showinfo("Результаты", "Пока нет решений.")
            return
        all_text = "\n\n".join(self.results_history)
        messagebox.showinfo("Все решения", all_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedTaskSolver(root)
    root.mainloop()
