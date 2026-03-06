# pyright: reportUnusedCallResult=false
import tkinter as tk
from tkinter import EW, NSEW, ttk
from tkinter import filedialog
from typing import Literal

from PIL import Image, ImageTk

type Mode = Literal[
        "selectFInterpolators",
        "selectGInterpolators",
        "None"
        ]

class ContourLinesInterface:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root

        self.f_interpolators: list[tuple[int, int]] = []
        self.g_interpolators: list[tuple[int, int]] = []

        self.mode: Mode = "None"

        self.mouse_x: int = 0
        self.mouse_y: int = 0

        self.layout_interface()


    def layout_interface(self):
        self.root.title("Lineas de Contorno")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.main_container: ttk.Frame = ttk.Frame(self.root)
        self.main_container.grid(column=0, row=0, sticky=NSEW)

        # Para adaptar al cambio de tamanio
        self.main_container.columnconfigure(0, weight=0)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        self.control_pane: ttk.Frame = ttk.Frame(self.main_container, relief="raised", padding=(10, 10))
        self.control_pane.grid(column=0, row=0, sticky=NSEW)

        # # Indicador de modo
        self.mode_indicator: ttk.Label = ttk.Label(self.control_pane, text="Mode: None", padding=(0, 4))
        self.mode_indicator.grid(column=0, row=0, sticky=EW)

        # Imagen
        self.add_image_button: ttk.Button = ttk.Button(self.control_pane, text="Add Image", command=self.load_image)
        self.add_image_button.grid(column=0, row=1, sticky=EW, pady=4)

        # Seleccionar nodos para f
        self.select_f_nodes_button: ttk.Button = ttk.Button(self.control_pane, text="Seleccionar nodos para f", command=lambda : self.set_mode("selectFInterpolators"))
        self.select_f_nodes_button.grid(column=0, row=2, sticky=EW, pady=4)

        # Seleccionar nodos para g
        self.select_g_nodes_button: ttk.Button = ttk.Button(self.control_pane, text="Seleccionar nodos para g", command=lambda: self.set_mode("selectGInterpolators"))
        self.select_g_nodes_button.grid(column=0, row=3, sticky=EW, pady=4)

        # Botton para generar funcion
        self.generate_function_button: ttk.Button = ttk.Button(self.control_pane, text="Generar funcion")
        self.generate_function_button.grid(column=0, row=4, sticky=EW, pady=4)

        # boton para ocultar imagen
        self.hide_image_button: ttk.Button = ttk.Button(self.control_pane, text="Ocultar Imagen")
        self.hide_image_button.grid(column=0, row=5, sticky=EW, pady=4)

        # boton para recetear nodos
        self.clear_nodes_button: ttk.Button = ttk.Button(self.control_pane, text="Limpiar Nodos")
        self.clear_nodes_button.grid(column=0, row=6, sticky=EW, pady=4)

        # Botton Calcular Area
        self.calculateAreaButton: ttk.Button = ttk.Button(self.control_pane, text="Calcular Area")
        self.calculateAreaButton.grid(column=0, row=7, sticky=EW, pady=4)
        self.resultLabel:ttk.Label = ttk.Label(self.control_pane, text="Area: ")
        self.resultLabel.grid(column=0, row=8, sticky=EW, pady=4)

        ## Canvas
        self.canvas_frame:ttk.Frame = ttk.Frame(self.main_container)
        self.canvas_frame.grid(column=1, row=0, sticky=NSEW)

        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        self.canvas: tk.Canvas = tk.Canvas(self.canvas_frame, background='white')
        self.canvas.grid(column=0, row=0, sticky=NSEW)

        self.canvas.bind("<Motion>", lambda e: self.mouse_move(e.x, e.y))
        self.canvas.bind("<Button-1>", lambda e: self.mouse_left_click(e.x, e.y))
        self.canvas.bind("<Button-2>", lambda e: self.mouse_right_click(e.x, e.y))

    def set_mode(self, mode: Mode):
        self.mode_indicator.configure(text=f"Mode: {mode}")
        self.mode = mode

    def mouse_move(self, x: int, y: int):
        self.mouse_x = x
        self.mouse_y = y

    def mouse_left_click(self, x: int, y: int):
        if(self.mode=="selectFInterpolators"):
            self.f_interpolators.append((x, y))
            self.render_interpolators()

        if(self.mode=="selectGInterpolators"):
            self.g_interpolators.append((x, y))

        self.render_interpolators()

    def mouse_right_click(self, x: int, y: int):
        if(self.mode=="selectFInterpolators"):
            self.f_interpolators.pop()
        if(self.mode=="selectGInterpolators"):
            self.g_interpolators.pop()

        self.render_interpolators()
        pass


    def render_interpolators(self):
        self.canvas.delete("f_interpolators")
        for x, y in self.f_interpolators:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="blue", tags=('f_interpolators'))

        self.canvas.delete("g_interpolators")
        for x, y in self.g_interpolators:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="green", tags=('g_interpolators'))

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # TODO: Manejar Error
            self.image_pil = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image_pil)
            self.canvas.delete("all")

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            required_width = max(canvas_width, self.image_pil.width)
            required_height = max(canvas_height, self.image_pil.height)
            self.canvas.config(width=required_width, height=required_height)
            #
            center_x = max(canvas_width, self.image_pil.width) / 2
            center_y = max(canvas_height, self.image_pil.height) / 2

            self.canvas.create_image(center_x, center_y, image=self.image_tk, anchor="center")
    pass


root = tk.Tk()
interface = ContourLinesInterface(root)
root.mainloop()
