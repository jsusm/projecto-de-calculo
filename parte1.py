# pyright: reportUnusedCallResult=false

import math
import tkinter as tk
from tkinter import EW, NSEW, ttk
from tkinter import filedialog
from typing import Literal
from PIL import Image, ImageTk
from calculateArea import calculate_area

type Mode = Literal[
        "selectA",
        "selectB",
        "selectC",
        "selectD",
        "SubintervalF",
        "SubintervalG",
        "selectFNodes",
        "selectGNodes",
        "None"
        ]

class AreaBetweenCurvesInterface:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Area Entre curvas")

        self.mode: Mode = "None"

        ## Valores de los entry de los intervalos en numeros
        self.a_value_number: float = 0
        self.b_value_number: float = 0
        self.c_value_number: float = 0
        self.d_value_number: float = 0

        ## Valores de estado para la seleccion visual de los intervalos
        self.a_selected: float = 0
        self.b_selected: float = 0
        self.c_selected: float = 0
        self.d_selected: float = 0

        ## Valores visuales de el intervalo con respecto a la imagen
        self.a_position: float = 0
        self.b_position: float = 0
        self.c_position: float = 0
        self.d_position: float = 0

        ## Subintervalos para F y G
        self.f_subintervals: list[tuple[int, int]] = []
        self.g_subintervals: list[tuple[int, int]] = []

        ## Puntos de interpolacion
        self.f_interpolators: list[tuple[int, int]] = []
        self.g_interpolators: list[tuple[int, int]] = []

        self.mouse_x: int = 0
        self.mouse_y: int = 0
        self.mouse_in: bool = False

        self.layout_interface()
        pass

    def setMode(self, mode: Mode):
        self.mode = mode
        self.mode_indicator.configure(text=f"Mode: {mode}")

    def layout_interface(self):
        # Para adaptar al cambio de tamanio
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_container: ttk.Frame = ttk.Frame(self.root)
        self.main_container.grid(column=0, row=0, sticky=NSEW)

        # Para adaptar al cambio de tamanio
        self.main_container.columnconfigure(0, weight=0)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        self.control_pane: ttk.Frame = ttk.Frame(self.main_container, relief="raised", padding=(10, 10))
        self.control_pane.grid(column=0, row=0, sticky=NSEW)

        # Indicador de modo
        self.mode_indicator: ttk.Label = ttk.Label(self.control_pane, text="Mode: Normal", padding=(0, 4))
        self.mode_indicator.grid(column=0, row=0, sticky=EW)

        # Imagen
        self.add_image_button: ttk.Button = ttk.Button(self.control_pane, text="Add Image", command=self.load_image)
        self.add_image_button.grid(column=0, row=1, sticky=EW)

        # Intervalos
        self.intervalFrame: ttk.Frame = ttk.Frame(self.control_pane, padding=(0, 10))
        self.intervalFrame.grid(column=0, row=2, sticky=EW)

        self.intervalLabel: ttk.Label = ttk.Label(self.intervalFrame, text="Intevalos", justify="left", padding=(0, 4))
        self.intervalLabel.grid(column=0, row=0, columnspan=3, sticky=EW)

        ## Intervalo [a,b]
        # (a)
        self.aValue: tk.StringVar = tk.StringVar()
        self.aValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="a: ", padding=2)
        self.aValueLable.grid(column=0, row=1)
        self.aEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4, textvariable=self.aValue)
        self.aEntry.grid(column=1, row=1)
        self.aAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar a", command=lambda: self.setMode("selectA"))
        self.aAdjustVisuallyButton.grid(column=2, row=1)

        # (b)
        self.bValue: tk.StringVar = tk.StringVar()
        self.bValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="b: ", padding=2)
        self.bValueLable.grid(column=0, row=2)
        self.bEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4, textvariable=self.bValue)
        self.bEntry.grid(column=1, row=2)
        self.bAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar b", command=lambda: self.setMode("selectB"))
        self.bAdjustVisuallyButton.grid(column=2, row=2)

        ## Intervalo [c,d]
        # (c)
        self.cValue: tk.StringVar = tk.StringVar()
        self.cValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="c: ", padding=2)
        self.cValueLable.grid(column=0, row=3)
        self.cEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4, textvariable=self.cValue)
        self.cEntry.grid(column=1, row=3)
        self.cAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar c", command=lambda: self.setMode("selectC"))
        self.cAdjustVisuallyButton.grid(column=2, row=3)


        # (d)
        self.dValue: tk.StringVar = tk.StringVar()
        self.dValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="d: ", padding=2)
        self.dValueLable.grid(column=0, row=4)
        self.dEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4, textvariable=self.dValue)
        self.dEntry.grid(column=1, row=4)
        self.dAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar d", command=lambda: self.setMode("selectD"))
        self.dAdjustVisuallyButton.grid(column=2, row=4)


        ## Herramientas
        self.toolsFrame: ttk.Frame = ttk.Frame(self.control_pane, padding=(0, 10))
        self.toolsFrame.grid(column=0, row=3, sticky=EW)

        self.toolsLabel: ttk.Label = ttk.Label(self.toolsFrame, text="Herramientas", justify="left")
        self.toolsLabel.grid(column=0, row=0, sticky=EW)

        self.f_submiterval : ttk.Button = ttk.Button(self.toolsFrame, text="Subintervalos Para f", command=lambda: self.setMode("SubintervalF"))
        self.f_submiterval.grid(column=0, row=1, pady=2, sticky=EW)

        self.gSubmiterval : ttk.Button = ttk.Button(self.toolsFrame, text="Subintervalos Para g", command=lambda: self.setMode("SubintervalG"))
        self.gSubmiterval.grid(column=0, row=2, pady=2, sticky=EW)

        self.fNodetool: ttk.Button = ttk.Button(self.toolsFrame, text="Seleccionar nodos para f", command=lambda: self.setMode("selectFNodes"))
        self.fNodetool.grid(column=0, row=3, pady=2)

        self.gNodetool: ttk.Button = ttk.Button(self.toolsFrame, text="Seleccionar nodos para g", command=lambda: self.setMode("selectGNodes"))
        self.gNodetool.grid(column=0, row=4, pady=2)

        # Botton Calcular Area
        self.calculateAreaButton: ttk.Button = ttk.Button(self.control_pane, text="Calcular Area", command=self.calculate_area)
        self.calculateAreaButton.grid(column=0, row=5, sticky=EW)
        self.resultLabel:ttk.Label = ttk.Label(self.control_pane, text="Area: ")
        self.resultLabel.grid(column=0, row=6, sticky=EW)

        ## Canvas
        self.canvas_frame:ttk.Frame = ttk.Frame(self.main_container)
        self.canvas_frame.grid(column=1, row=0, sticky=NSEW)


        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        self.canvas: tk.Canvas = tk.Canvas(self.canvas_frame, background='white')
        self.canvas.grid(column=0, row=0, sticky=NSEW)
        ## Enlasar eventos con el canvas
        self.canvas.bind("<Motion>", lambda e: self.mouse_move(e.x, e.y))
        self.canvas.bind("<Enter>", lambda _: self.mouse_enter())
        self.canvas.bind("<Leave>", lambda _: self.mouse_leave())
        self.canvas.bind("<Button-1>", lambda e: self.mouse_left_click(e.x, e.y))
        self.canvas.bind("<Button-3>", lambda e: self.mouse_right_click(e.x, e.y))

        # self.dev_setup()
    pass

    def create_subinterval_line(self, x:int, y:int, tag: str, dashed: bool = False, color: str = "blue"):
        self.canvas.create_oval(x - 4, y - 4,x + 4, y + 4, fill=color, tags=(tag))
        if(dashed):
            self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), fill=color, tags=(tag), dash=(10,4))
        else:
            self.canvas.create_line(x, 0, x, self.canvas.winfo_height(), fill=color, tags=(tag))


    def boundary_from_mode(self):
        if(self.mode == "selectA"): return 'a'
        if(self.mode == "selectB"): return 'b'
        if(self.mode == "selectC"): return 'c'
        if(self.mode == "selectD"): return 'd'
        return "-"

    def render_subintervals(self):
        ## render f subintervals
        self.canvas.delete("f_subintervals")
        for x, y in self.f_subintervals:
            self.create_subinterval_line(x, y,"f_subintervals",  True)

        ## render g subintervals
        self.canvas.delete("g_subintervals")
        for x, y in self.g_subintervals:
            self.create_subinterval_line(x, y,"g_subintervals",  True, color="green")

    def render_interpolators(self):
        self.canvas.delete("f_interpolators")
        for x, y in self.f_interpolators:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="blue", tags=('f_interpolators'))

        self.canvas.delete("g_interpolators")
        for x, y in self.g_interpolators:
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="green", tags=('g_interpolators'))

    def mouse_enter(self):
        self.mouse_in = True

    def mouse_leave(self):
        self.mouse_in = False
        self.render_state()

    def mouse_move(self, x: int, y: int):
        self.mouse_x = x
        self.mouse_y = y
        self.render_state()
        pass

    def is_selecting_interval_boundary_mode(self):
        return self.mode in ['selectA', 'selectB', 'selectC', 'selectD']

    def mouse_left_click(self, x: int, y: int):
        ###### Limites de intervalos ######
        bounday = self.boundary_from_mode()
        if(self.mouse_in and bounday != '-'):
            vertical_line = False
            if(self.mode == "selectA"):
                self.a_selected = True
                self.a_position = x

            if(self.mode == "selectB"):
                self.b_selected = True
                self.b_position = x

            if(self.mode == "selectC"):
                self.c_selected = True
                self.c_position = y
                vertical_line = True

            if(self.mode == "selectD"):
                self.d_selected = True
                self.d_position = y
                vertical_line = True

            linetag = f"{bounday}line"
            self.canvas.delete(linetag)
            if(vertical_line):
                self.canvas.create_line(0, self.mouse_y, self.canvas.winfo_width(), self.mouse_y, fill="#aaa", tags=(linetag), dash=(10, 4))
                self.canvas.create_text(10, y, text=bounday, tags=(linetag))
            else:
                self.canvas.create_line(self.mouse_x, 0, self.mouse_x, self.canvas.winfo_height(), fill="#aaa", tags=(linetag), dash=(10, 4))
                self.canvas.create_text(x, 10, text=bounday, tags=(linetag))

        ###### Subintervalos ######
        if(self.mode == "SubintervalF"):
            if(len(self.f_subintervals) >= 3):
                self.f_subintervals.pop(0)
            self.f_subintervals.append((x, y))

            self.canvas.delete("f_subinterval") # quitar la linea dibujada para seleccionar
            self.render_subintervals()

        if(self.mode == "SubintervalG"):
            if(len(self.g_subintervals) >= 3):
                self.g_subintervals.pop(0)
            self.g_subintervals.append((x, y))

            self.canvas.delete("g_subinterval") # quitar la linea dibujada para seleccionar
            self.render_subintervals()

        if(self.mode == "selectFNodes"):
            self.f_interpolators.append((x, y))
            self.render_interpolators()

        if(self.mode == "selectGNodes"):
            self.g_interpolators.append((x, y))
            self.render_interpolators()

        pass


    def mouse_right_click(self, x: int, y: int):
        ## Desseleccinar si cliqueas el click derecho
        if(self.mouse_in):
            if(self.mode == "selectA"): self.a_selected = False
            if(self.mode == "selectB"): self.b_selected = False
            if(self.mode == "selectC"): self.c_selected = False
            if(self.mode == "selectD"): self.d_selected = False
        self.render_state()

        ## Quitar el ultimo "subintervalo" si clickeas el click derecho
        if(self.mode == "SubintervalF"):
            if(len(self.f_subintervals)):
                self.f_subintervals.pop()

            self.render_subintervals()

        if(self.mode == "SubintervalG"):
            if(len(self.g_subintervals)):
                self.g_subintervals.pop()

            self.render_subintervals()

        if(self.mode == "selectFNodes"):
            if(len(self.f_interpolators)):
                self.f_interpolators.pop()

            self.render_interpolators()

        if(self.mode == "selectGNodes"):
            if(len(self.g_interpolators)):
                self.g_interpolators.pop()

            self.render_interpolators()
        pass

    def render_state(self):
        ###### Limites de intervalos ######
        ## Si ya esta selecionada la barrera del intervalo no hace falta redibujar la linea
        draw_line = False
        if(self.mode == "selectA"):
            draw_line = not self.a_selected
        if(self.mode == "selectB"):
            draw_line = not self.b_selected
        if(self.mode == "selectC"):
            draw_line = not self.c_selected
        if(self.mode == "selectD"):
            draw_line = not self.d_selected

        if(self.is_selecting_interval_boundary_mode() and self.mouse_in):
            vertical_line = False
            bounday = self.boundary_from_mode()

            if(self.mode == "selectC"):
                vertical_line = True
            if(self.mode == "selectD"):
                vertical_line = True

            linetag = f"{bounday}line"
            if(draw_line):
                self.canvas.delete(linetag)
                if(vertical_line):
                    self.canvas.create_line(0, self.mouse_y, self.canvas.winfo_width(), self.mouse_y, fill="red", tags=(linetag))
                else:
                    self.canvas.create_line(self.mouse_x, 0, self.mouse_x, self.canvas.winfo_height(), fill="red", tags=(linetag))

        # Borrar las lineas cuando el mouse deja el canvas
        elif(self.is_selecting_interval_boundary_mode() and not self.mouse_in):
            bounday = self.boundary_from_mode()
            linetag = f"{bounday}line"
            if(draw_line): self.canvas.delete(linetag)

        ###### Subintervalos ######
        if(self.mode == "SubintervalF" and not len(self.f_subintervals) > 3 and self.mouse_in):
            self.canvas.delete("f_subinterval")
            self.create_subinterval_line(self.mouse_x, self.mouse_y, "f_subinterval")

        if(self.mode == "SubintervalF" and not self.mouse_in):
            self.canvas.delete("f_subinterval")


        if(self.mode == "SubintervalG" and not len(self.g_subintervals) > 3 and self.mouse_in):
            self.canvas.delete("g_subinterval")
            self.create_subinterval_line(self.mouse_x, self.mouse_y, "g_subinterval", color="green")

        if(self.mode == "SubintervalG" and not self.mouse_in):
            self.canvas.delete("g_subinterval")

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

            self.a_selected = False
            self.b_selected = False
            self.c_selected = False
            self.d_selected = False
            self.aValue.set("")
            self.bValue.set("")
            self.cValue.set("")
            self.dValue.set("")
            self.f_subintervals = []
            self.g_subintervals = []
            self.f_interpolators = []
            self.g_interpolators = []
            self.render_interpolators()
            self.render_subintervals()
            self.canvas.delete("aline")
            self.canvas.delete("bline")
            self.canvas.delete("cline")
            self.canvas.delete("dline")

    def calculate_function_area(self, raw_interpolators: list[tuple[int, int]], raw_subintervals: list[tuple[int, int]]):
        self.a_value_number = float(self.aValue.get())
        self.b_value_number = float(self.bValue.get())
        self.c_value_number = float(self.cValue.get())
        self.d_value_number = float(self.dValue.get())

        # Relativisamos los puntos dentro de los intervalos
        # (x - a)/(a - b) * (A - B) + A
        # donde x es el valor del punto
        # a es el limite visual inferior del intervalo
        # b es el limite visual superior del intervalo
        # A es el limite real inferior
        # B es el limite real superior

        A = self.a_value_number
        B = self.b_value_number
        C = self.c_value_number
        D = self.d_value_number

        a = self.a_position
        b = self.b_position
        c = self.c_position
        d = self.d_position

        interpolators: list[tuple[float, float]] = []
        # incluimos los puntos de interpolacion
        for i in raw_interpolators:
            print(i)
            x = ((i[0] - a) / (b - a)) * (B - A) + A
            y = ((i[1] - c) / (d - c)) * (D - C) + C
            interpolators.append((x, y))

        ## subintervalos en las cordendas transformadas
        ## aniadimos a como frontera del primer intervalo
        subintervals: list[float] = [A]
        # incluimos los nodos de las fronteras de los subintervalos
        for i in raw_subintervals:
            x = ((i[0] - a) / (b - a)) * (B - A) + A
            y = ((i[1] - c) / (d - c)) * (D - C) + C
            interpolators.append((x, y))
            subintervals.append(x)

        # aniadimos B para completar el ultimo subintervalo
        subintervals.append(B)

        # No hace falta ordenarlos, pero es por el toc
        interpolators = sorted(interpolators, key=lambda x: x[0])

        # sumamos las areas de los intervalos
        area = 0
        for i in range(len(subintervals) - 1):
            subinterval_interpolators = [p for p in interpolators if p[0] >= subintervals[i] and p[0] <= subintervals[i+1]]
            print("i:", subinterval_interpolators)

            area += calculate_area(subinterval_interpolators, subintervals[i], subintervals[i+1])

        return area


    def calculate_area(self):
        f_area = self.calculate_function_area(self.f_interpolators, self.f_subintervals)
        print("f area: ", f_area)

        g_area = self.calculate_function_area(self.g_interpolators, self.g_subintervals)
        print("g area: ", g_area)

        area_between_curves = math.fabs(f_area - g_area)
        self.resultLabel.configure(text=f"Area: {area_between_curves:.8f}")



root = tk.Tk()
interface = AreaBetweenCurvesInterface(root)
root.mainloop()
