import tkinter as tk
from tkinter import colorchooser, filedialog
import json


class Shape:
    def __init__(self, canvas, shape_type, coords, outline='black', fill='', width=2):
        self.canvas = canvas
        self.shape_type = shape_type
        self.coords = coords
        self.outline = outline
        self.fill = fill
        self.width = width
        self.id = self.draw()

    def draw(self):
        if self.shape_type == 'line':
            return self.canvas.create_line(*self.coords, fill=self.outline, width=self.width)
        elif self.shape_type == 'rectangle':
            return self.canvas.create_rectangle(*self.coords, outline=self.outline, fill=self.fill, width=self.width)
        elif self.shape_type == 'oval':
            return self.canvas.create_oval(*self.coords, outline=self.outline, fill=self.fill, width=self.width)
        elif self.shape_type == 'pen':
            return self.canvas.create_line(self.coords, fill=self.outline, width=self.width, smooth=True)

    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)
        self.coords = [(x + dx, y + dy) for x, y in self.coords] if self.shape_type == 'pen' else (
            self.coords[0] + dx, self.coords[1] + dy, self.coords[2] + dx, self.coords[3] + dy)

    def resize(self, dx, dy):
        if self.shape_type in ('rectangle', 'oval', 'line'):
            x0, y0, x1, y1 = self.coords
            self.coords = (x0, y0, x1 + dx, y1 + dy)
            self.canvas.coords(self.id, *self.coords)

    def to_dict(self):
        return {
            'type': self.shape_type,
            'coords': self.coords,
            'outline': self.outline,
            'fill': self.fill,
            'width': self.width
        }


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор с Пером")
        self.shapes = []
        self.selected_shape = None
        self.current_tool = 'line'
        self.bg_color = 'white'
        self.start = None
        self.color = 'black'
        self.fill_color = ''
        self.pen_points = []

        self.create_ui()
        self.setup_bindings()

    def create_ui(self):
        self.toolbar = tk.Frame(self.root, bg='lightgrey')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        for tool in ['line', 'rectangle', 'oval', 'pen']:
            tk.Button(self.toolbar, text=tool.title(), command=lambda t=tool: self.set_tool(t)).pack(side=tk.LEFT)

        tk.Button(self.toolbar, text='Цвет', command=self.choose_color).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Заливка', command=self.choose_fill).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Фон', command=self.change_bg).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Сохранить', command=self.save).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Загрузить', command=self.load).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.root, bg=self.bg_color, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def setup_bindings(self):
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def set_tool(self, tool):
        self.current_tool = tool

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    def choose_fill(self):
        fill = colorchooser.askcolor()[1]
        if fill:
            self.fill_color = fill

    def change_bg(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.canvas.config(bg=color)

    def on_click(self, event):
        self.start = (event.x, event.y)
        self.selected_shape = self.get_shape_at(event.x, event.y)
        if self.current_tool == 'pen':
            self.pen_points = [(event.x, event.y)]

    def on_drag(self, event):
        if self.current_tool == 'pen':
            self.pen_points.append((event.x, event.y))
            self.canvas.create_line(self.pen_points[-2], self.pen_points[-1], fill=self.color, width=2, smooth=True)
        elif self.selected_shape:
            dx = event.x - self.start[0]
            dy = event.y - self.start[1]
            self.selected_shape.move(dx, dy)
            self.start = (event.x, event.y)

    def on_release(self, event):
        if self.current_tool == 'pen':
            shape = Shape(self.canvas, 'pen', self.pen_points, self.color)
            self.shapes.append(shape)
        elif not self.selected_shape and self.start:
            coords = (*self.start, event.x, event.y)
            shape = Shape(self.canvas, self.current_tool, coords, self.color, self.fill_color)
            self.shapes.append(shape)
        self.selected_shape = None
        self.start = None

    def get_shape_at(self, x, y):
        for shape in reversed(self.shapes):
            if self.canvas.find_withtag('current') == (shape.id,):
                return shape
        return None

    def save(self):
        data = {
            'bg': self.bg_color,
            'shapes': [s.to_dict() for s in self.shapes]
        }
        file = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON файлы', '*.json')])
        if file:
            with open(file, 'w') as f:
                json.dump(data, f)

    def load(self):
        file = filedialog.askopenfilename(filetypes=[('JSON файлы', '*.json')])
        if file:
            with open(file, 'r') as f:
                data = json.load(f)
            self.canvas.delete('all')
            self.shapes.clear()
            self.bg_color = data.get('bg', 'white')
            self.canvas.config(bg=self.bg_color)
            for shape_data in data['shapes']:
                shape = Shape(self.canvas, **shape_data)
                self.shapes.append(shape)


if __name__ == '__main__':
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
