# pyright: reportUnusedCallResult=false

import tkinter as tk
from tkinter import EW, NSEW, ttk
class AreaBetweenCurvesInterface:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Area Entre curvas")

        self.layoutInterface()
        pass

    def layoutInterface(self):
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

        # Imagen
        self.add_image_button: ttk.Button = ttk.Button(self.control_pane, text="Add Image")
        self.add_image_button.grid(column=0, row=0, sticky=EW)

        # Intervalos
        self.intervalFrame: ttk.Frame = ttk.Frame(self.control_pane, padding=(0, 10))
        self.intervalFrame.grid(column=0, row=1, sticky=EW)

        self.intervalLabel: ttk.Label = ttk.Label(self.intervalFrame, text="Intevalos", justify="left", padding=(0, 4))
        self.intervalLabel.grid(column=0, row=0, columnspan=3, sticky=EW)

        ## Intervalo [a,b]
        # (a)
        self.aValue: tk.StringVar = tk.StringVar()
        self.aValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="a: ", padding=2)
        self.aValueLable.grid(column=0, row=1)
        self.aEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4)
        self.aEntry.grid(column=1, row=1)
        self.aAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar a")
        self.aAdjustVisuallyButton.grid(column=2, row=1)

        # (b)
        self.bValue: tk.StringVar = tk.StringVar()
        self.bValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="b: ", padding=2)
        self.bValueLable.grid(column=0, row=2)
        self.bEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4)
        self.bEntry.grid(column=1, row=2)
        self.bAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar b")
        self.bAdjustVisuallyButton.grid(column=2, row=2)

        ## Intervalo [c,d]
        # (c)
        self.cValue: tk.StringVar = tk.StringVar()
        self.cValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="c: ", padding=2)
        self.cValueLable.grid(column=0, row=3)
        self.cEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4)
        self.cEntry.grid(column=1, row=3)
        self.cAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar c")
        self.cAdjustVisuallyButton.grid(column=2, row=3)


        # (d)
        self.dValue: tk.StringVar = tk.StringVar()
        self.dValueLable: ttk.Label = ttk.Label(self.intervalFrame, text="d: ", padding=2)
        self.dValueLable.grid(column=0, row=4)
        self.dEntry: ttk.Entry = ttk.Entry(self.intervalFrame, width=4)
        self.dEntry.grid(column=1, row=4)
        self.dAdjustVisuallyButton: ttk.Button = ttk.Button(self.intervalFrame, text="Ajustar d")
        self.dAdjustVisuallyButton.grid(column=2, row=4)


        ## Herramientas
        self.toolsFrame: ttk.Frame = ttk.Frame(self.control_pane, padding=(0, 10))
        self.toolsFrame.grid(column=0, row=2, sticky=EW)

        self.toolsLabel: ttk.Label = ttk.Label(self.toolsFrame, text="Herramientas", justify="left")
        self.toolsLabel.grid(column=0, row=0, sticky=EW)

        self.fNodetool: ttk.Button = ttk.Button(self.toolsFrame, text="Seleccionar nodos para f")
        self.fNodetool.grid(column=0, row=1, pady=2)

        self.gNodetool: ttk.Button = ttk.Button(self.toolsFrame, text="Seleccionar nodos para g")
        self.gNodetool.grid(column=0, row=2, pady=2)

        # Calcular Area

        self.calculateAreaButton: ttk.Button = ttk.Button(self.control_pane, text="Calcular Area")
        self.calculateAreaButton.grid(column=0, row=4, sticky=EW)
        self.resultLabel:ttk.Label = ttk.Label(self.control_pane, text="Area: ")
        self.resultLabel.grid(column=0, row=5, sticky=EW)

        ## Canvas
        self.canvas_frame:ttk.Frame = ttk.Frame(self.main_container)
        self.canvas_frame.grid(column=1, row=0, sticky=NSEW)

        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        self.canvas: tk.Canvas = tk.Canvas(self.canvas_frame, background='white')
        self.canvas.grid(column=0, row=0, sticky=NSEW)
    pass


root = tk.Tk()
interface = AreaBetweenCurvesInterface(root)
root.mainloop()
