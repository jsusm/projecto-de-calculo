import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class ContourLinesInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz para Curvas de Nivel")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{int(screen_width*0.8)}x{int(screen_height*0.8)}")

        self.puntos_f = []
        self.puntos_g = []
        self.modo = "f"
        self.image_pil = None
        self.image_tk = None
        self.puntos_ids = []

        self.interfaceDesign()

    def interfaceDesign(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        self.panel_control = tk.Frame(self.main_container, width=250, bg="lightgray", padx=10, pady=10)
        self.panel_control.pack(side="left", fill="y")
        self.panel_control.pack_propagate(False)

        tk.Button(self.panel_control, text="Add Image", command=self.load_image).pack(fill="x", pady=5)

        self.modo_button = tk.Button(self.panel_control, text="Cambiar a Funcion G", command=self.cambiar_modo)
        self.modo_button.pack(fill="x", pady=5)

        self.eliminar_button = tk.Button(self.panel_control, text="Eliminar Ultimo Punto", command=self.eliminar_ultimo_punto_y_despintar)
        self.eliminar_button.pack(fill="x", pady=5)

        tk.Label(self.panel_control, text="Subintervalos (x)", bg="lightgray").pack(pady=(15, 0))

        self.frame_sub = tk.Frame(self.panel_control, bg="lightgray")
        self.frame_sub.pack(fill="x")

        tk.Label(self.frame_sub, text="x1:", bg="lightgray").grid(row=0, column=0)
        self.entry_x1 = tk.Entry(self.frame_sub, width=10)
        self.entry_x1.grid(row=0, column=1, pady=2)

        tk.Label(self.frame_sub, text="x2:", bg="lightgray").grid(row=1, column=0)
        self.entry_x2 = tk.Entry(self.frame_sub, width=10)
        self.entry_x2.grid(row=1, column=1, pady=2)

        tk.Frame(self.panel_control, bg="lightgray").pack(expand=True, fill="both")

        tk.Button(self.panel_control, text="Calcular Area", command=self.pasar_parametros).pack(fill="x", pady=10)

        self.canvas_frame = tk.Frame(self.main_container)
        self.canvas_frame.pack(side="right", fill="both", expand=True)

        self.hbar = tk.Scrollbar(self.canvas_frame, orient="horizontal")
        self.hbar.pack(side="bottom", fill="x")
        self.vbar = tk.Scrollbar(self.canvas_frame, orient="vertical")
        self.vbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", cursor="cross",
                                xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.hbar.config(command=self.canvas.xview)
        self.vbar.config(command=self.canvas.yview)

        # Creación del Label que irá sobre la imagen
        self.label_modo = tk.Label(self.root, text="Seleccionando Puntos en f", bg="white", font=("Arial", 12), fg="black")

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_pil = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image_pil)
            self.canvas.delete("all")
            self.puntos_f = []
            self.puntos_g = []
            self.puntos_ids = []

            self.canvas.config(scrollregion=(0, 0, self.image_pil.width, self.image_pil.height))
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            center_x = max(canvas_width, self.image_pil.width) / 2
            center_y = max(canvas_height, self.image_pil.height) / 2

            self.canvas.create_image(center_x, center_y, anchor="center", image=self.image_tk)

            #Reposicionar el Label de modo también en relación al nuevo centro
            self.canvas.create_window(center_x, center_y - (self.image_pil.height/2) + 20, 
                                     window=self.label_modo, anchor="n", tags="ui_label")

    def cambiar_modo(self):
        if self.modo == "f":
            self.modo = "g"
            self.label_modo.config(text="Seleccionando Puntos en g")
            self.modo_button.config(text="Cambiar a Funcion F")
        else:
            self.modo = "f"
            self.label_modo.config(text="Seleccionando Puntos en f")
            self.modo_button.config(text="Cambiar a Funcion G")

    def on_canvas_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        color = "red" if self.modo == "f" else "purple"
        punto_id = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="black")

        if self.modo == "f":
            self.puntos_f.append((x, y))
        else:
            self.puntos_g.append((x, y))

        self.puntos_ids.append((punto_id, self.modo))

    def eliminar_ultimo_punto_y_despintar(self):
        if self.puntos_ids:
            last_id, modo_punto = self.puntos_ids.pop()
            self.canvas.delete(last_id)
            if modo_punto == "f":
                self.puntos_f.pop()
            else:
                self.puntos_g.pop()

    def pasar_parametros(self):
        x1 = self.entry_x1.get()
        x2 = self.entry_x2.get()
        calculateArea.calculate_area(self.puntos_f, self.puntos_g, x1, x2)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContourLinesInterface(root)
    root.mainloop()
