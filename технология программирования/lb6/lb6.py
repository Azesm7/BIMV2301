import tkinter as tk
import math
import random

class BilliardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Абсолютно упругое тело — симуляция на Canvas")

        # Конфигурация поля
        self.canvas_width = 600
        self.canvas_height = 400
        self.ball_radius = 15

        # Холст
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="darkgreen")
        self.canvas.pack()

        # Панель управления
        controls = tk.Frame(root)
        controls.pack(fill='x')

        # Ползунок скорости
        tk.Label(controls, text="Скорость анимации:").grid(row=0, column=0)
        self.speed = tk.IntVar(value=50)
        self.speed_scale = tk.Scale(controls, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.speed)
        self.speed_scale.grid(row=0, column=1)

        # Начальная скорость
        tk.Label(controls, text="Начальная скорость:").grid(row=1, column=0)
        self.input_speed = tk.Entry(controls, width=5)
        self.input_speed.insert(0, "5")
        self.input_speed.grid(row=1, column=1)

        # Начальный угол (градусы)
        tk.Label(controls, text="Начальный угол (град.):").grid(row=1, column=2)
        self.input_angle = tk.Entry(controls, width=5)
        self.input_angle.insert(0, "45")
        self.input_angle.grid(row=1, column=3)

        # Кнопка Старт/Пауза
        self.start_btn = tk.Button(controls, text="Пуск", command=self.toggle_run)
        self.start_btn.grid(row=1, column=4, padx=10)

        # Метка для текущего состояния
        self.status_label = tk.Label(controls, text="Остановлено")
        self.status_label.grid(row=1, column=5)

        # Отображение координат и скорости
        self.info_label = tk.Label(root, text="x=0 y=0 | dx=0 dy=0", font=("Consolas", 10))
        self.info_label.pack()

        # Шар
        self.ball = self.canvas.create_oval(0, 0, self.ball_radius * 2, self.ball_radius * 2, fill="white")
        self.x = random.randint(100, 500)
        self.y = random.randint(100, 300)
        self.dx = 0
        self.dy = 0
        self.running = False

        # Инициализация позиции
        self.update_ball()
        self.animate()

    def toggle_run(self):
        if not self.running:
            try:
                speed = float(self.input_speed.get())
                angle_deg = float(self.input_angle.get())
                angle_rad = math.radians(angle_deg)

                # Расчёт векторов скорости
                self.dx = speed * math.cos(angle_rad)
                self.dy = speed * math.sin(angle_rad)
                self.running = True
                self.status_label.config(text="Работает")
                self.start_btn.config(text="Пауза")
            except ValueError:
                self.status_label.config(text="Ошибка ввода")
        else:
            self.running = False
            self.status_label.config(text="Пауза")
            self.start_btn.config(text="Пуск")

    def update_ball(self):
        self.canvas.coords(
            self.ball,
            self.x,
            self.y,
            self.x + self.ball_radius * 2,
            self.y + self.ball_radius * 2
        )
        self.info_label.config(text=f"x={int(self.x)} y={int(self.y)} | dx={self.dx:.2f} dy={self.dy:.2f}")

    def animate(self):
        if self.running:
            self.x += self.dx
            self.y += self.dy

            # Отражение от стен
            if self.x <= 0 or self.x >= self.canvas_width - self.ball_radius * 2:
                self.dx *= -1
            if self.y <= 0 or self.y >= self.canvas_height - self.ball_radius * 2:
                self.dy *= -1

            self.update_ball()

        delay = 101 - self.speed.get()
        self.root.after(delay, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = BilliardApp(root)
    root.mainloop()
