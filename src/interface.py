import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from charts import heatmap_IMC_vs_sueño, scatter_IMC_vs_sueño, steps_sleep_chart

class GraphSelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selector de Gráficas - Análisis de Sueño")
        self.geometry("600x400")
        self.minsize(500, 350)
        self.data = None
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="Visualización de Datos de Sueño", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Frame para cargar datos
        load_frame = ttk.LabelFrame(main_frame, text="Cargar Datos", padding=10)
        load_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_label = ttk.Label(load_frame, text="No hay datos cargados", 
                                    foreground="red")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        btn_load = ttk.Button(load_frame, text="Cargar CSV/Excel", 
                             command=self.load_data)
        btn_load.pack(side=tk.RIGHT, padx=5)
        
        # Frame para seleccionar gráfica
        graph_frame = ttk.LabelFrame(main_frame, text="Seleccionar Gráfica", padding=15)
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variable para radio buttons
        self.graph_choice = tk.StringVar(value="heatmap")
        
        # Radio buttons para cada gráfica
        rb1 = ttk.Radiobutton(graph_frame, 
                             text="Heatmap - IMC vs Duración del Sueño",
                             variable=self.graph_choice, 
                             value="heatmap")
        rb1.pack(anchor=tk.W, pady=8)
        
        rb2 = ttk.Radiobutton(graph_frame, 
                             text="Scatter Plot - IMC vs Duración del Sueño",
                             variable=self.graph_choice, 
                             value="scatter")
        rb2.pack(anchor=tk.W, pady=8)
        
        rb3 = ttk.Radiobutton(graph_frame, 
                             text="Gráfica de Barras - Pasos Diarios vs Calidad del Sueño",
                             variable=self.graph_choice, 
                             value="steps")
        rb3.pack(anchor=tk.W, pady=8)
        
        # Botón para mostrar gráfica
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        self.btn_show = ttk.Button(btn_frame, text="Mostrar Gráfica", 
                                   command=self.show_graph, 
                                   state=tk.DISABLED)
        self.btn_show.pack(side=tk.LEFT, padx=5)
        
        btn_exit = ttk.Button(btn_frame, text="Salir", command=self.quit)
        btn_exit.pack(side=tk.LEFT, padx=5)
        
        # Barra de estado
        self.status = tk.StringVar(value="Listo. Cargue los datos para comenzar.")
        statusbar = ttk.Label(self, textvariable=self.status, 
                             relief=tk.SUNKEN, anchor=tk.W, padding=(4,2))
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_data(self):
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    self.data = pd.read_csv(filename)
                elif filename.endswith('.xlsx'):
                    self.data = pd.read_excel(filename)
                else:
                    messagebox.showerror("Error", "Formato de archivo no soportado")
                    return
                
                self.file_label.config(text=f"✓ Datos cargados: {filename.split('/')[-1]}", 
                                      foreground="green")
                self.btn_show.config(state=tk.NORMAL)
                self.status.set(f"Datos cargados: {len(self.data)} registros")
                messagebox.showinfo("Éxito", f"Datos cargados correctamente\nRegistros: {len(self.data)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
                self.status.set("Error al cargar datos")
    
    def show_graph(self):
        if self.data is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar los datos")
            return
        
        choice = self.graph_choice.get()
        
        try:
            if choice == "heatmap":
                self.status.set("Mostrando: Heatmap IMC vs Sueño")
                heatmap_IMC_vs_sueño(self.data)
                
            elif choice == "scatter":
                self.status.set("Mostrando: Scatter Plot IMC vs Sueño")
                scatter_IMC_vs_sueño(self.data)
                
            elif choice == "steps":
                # Para esta gráfica necesitamos procesar los datos primero
                self.status.set("Mostrando: Pasos Diarios vs Calidad del Sueño")
                # Aquí asumimos que tienes la función que procesa los datos
                # Si necesitas procesar los datos de manera diferente, ajusta aquí
                steps_sleep_chart(self.data)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la gráfica:\n{str(e)}")
            self.status.set("Error al mostrar gráfica")

class MiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mi Interfaz Tkinter")
        self.geometry("800x500")
        self.minsize(600, 400)
        self.create_menu()
        self.create_toolbar()
        self.create_main_area()
        self.create_statusbar()

    def create_menu(self):
        menubar = tk.Menu(self)
        # Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.on_nuevo)
        file_menu.add_command(label="Guardar", command=self.on_guardar)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de...", command=self.on_acerca)
        menubar.add_cascade(label="Ayuda", menu=help_menu)

        self.config(menu=menubar)

    def create_toolbar(self):
        toolbar = ttk.Frame(self, padding=(4,4))
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_nuevo = ttk.Button(toolbar, text="Nuevo", command=self.on_nuevo)
        btn_guardar = ttk.Button(toolbar, text="Guardar", command=self.on_guardar)
        btn_modal = ttk.Button(toolbar, text="Dialogo", command=self.on_mostrar_dialogo)

        btn_nuevo.pack(side=tk.LEFT, padx=2)
        btn_guardar.pack(side=tk.LEFT, padx=2)
        btn_modal.pack(side=tk.LEFT, padx=2)

    def create_main_area(self):
        container = ttk.Frame(self, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Dividir en columnas con panedwindow para redimensionar
        paned = ttk.Panedwindow(container, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(paned, width=300)
        right = ttk.Frame(paned)

        paned.add(left, weight=1)
        paned.add(right, weight=3)

        # Left: Formulario
        frm = ttk.LabelFrame(left, text="Formulario")
        frm.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        ttk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        self.entry_nombre = ttk.Entry(frm)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.EW, padx=4, pady=4)

        ttk.Label(frm, text="Edad:").grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        self.spin_edad = ttk.Spinbox(frm, from_=0, to=120)
        self.spin_edad.grid(row=1, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(frm, text="Rol:").grid(row=2, column=0, sticky=tk.W, padx=4, pady=4)
        self.combo_rol = ttk.Combobox(frm, values=["Estudiante", "Profesor", "Investigador", "Otro"])
        self.combo_rol.grid(row=2, column=1, sticky=tk.EW, padx=4, pady=4)

        # Botones del formulario
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(8,0))
        ttk.Button(btn_frame, text="Agregar a la lista", command=self.on_agregar).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Limpiar", command=self.on_limpiar).pack(side=tk.LEFT, padx=4)

        # Make columns expand nicely
        frm.columnconfigure(1, weight=1)

        # Right: Lista y detalles
        list_frame = ttk.LabelFrame(right, text="Lista de usuarios")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.listbox = tk.Listbox(list_frame, exportselection=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4,0), pady=4)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_listbox)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0,4))
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Panel de detalles
        detail_frame = ttk.Frame(right)
        detail_frame.pack(fill=tk.X, padx=6, pady=(0,6))
        ttk.Label(detail_frame, text="Detalles:").grid(row=0, column=0, sticky=tk.W)
        self.lbl_detalles = ttk.Label(detail_frame, text="Seleccione un elemento de la lista", anchor=tk.W)
        self.lbl_detalles.grid(row=1, column=0, sticky=tk.EW)
        detail_frame.columnconfigure(0, weight=1)

    def create_statusbar(self):
        self.status = tk.StringVar(value="Listo")
        statusbar = ttk.Label(self, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W, padding=(4,2))
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Callbacks ---
    def on_nuevo(self):
        self.on_limpiar()
        self.status.set("Nuevo formulario listo")

    def on_guardar(self):
        # Ejemplo simple: guardar lista en un archivo
        try:
            items = self.listbox.get(0, tk.END)
            with open("usuarios.txt", "w", encoding="utf-8") as f:
                for it in items:
                    f.write(it + "\n")
            self.status.set(f"Guardados {len(items)} usuarios en usuarios.txt")
            messagebox.showinfo("Guardar", "Guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def on_mostrar_dialogo(self):
        respuesta = simpledialog.askstring("Pregunta", "¿Cómo te llamas?")
        if respuesta:
            messagebox.showinfo("Hola", f"Hola, {respuesta}!")
            self.status.set(f"Saludado: {respuesta}")

    def on_agregar(self):
        nombre = self.entry_nombre.get().strip()
        edad = self.spin_edad.get().strip()
        rol = self.combo_rol.get().strip()

        # Validación básica
        if not nombre:
            messagebox.showwarning("Validación", "El campo 'Nombre' es obligatorio.")
            self.status.set("Error: nombre vacío")
            return
        try:
            edad_val = int(edad)
            if edad_val < 0 or edad_val > 120:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validación", "Edad inválida.")
            self.status.set("Error: edad inválida")
            return

        item = f"{nombre} — {edad_val} años — {rol or '—'}"
        self.listbox.insert(tk.END, item)
        self.status.set(f"Agregado: {nombre}")
        self.on_limpiar_fields(keep_role=True)

    def on_limpiar_fields(self, keep_role=False):
        self.entry_nombre.delete(0, tk.END)
        self.spin_edad.delete(0, tk.END)
        self.spin_edad.insert(0, "18")
        if not keep_role:
            self.combo_rol.set("")

    def on_limpiar(self):
        self.on_limpiar_fields()
        self.listbox.delete(0, tk.END)
        self.lbl_detalles.config(text="Seleccione un elemento de la lista")
        self.status.set("Formulario y lista limpiados")

    def on_select_listbox(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        text = self.listbox.get(sel[0])
        self.lbl_detalles.config(text=text)
        self.status.set(f"Seleccionado: {text.split('—', 1)[0].strip()}")

if __name__ == "__main__":
    # Usar la nueva interfaz de gráficas
    app = GraphSelectorApp()
    app.mainloop()
    
    # Si quieres usar la interfaz antigua de formulario, descomenta las siguientes líneas:
    # app = MiApp()
    # app.spin_edad.delete(0, tk.END); app.spin_edad.insert(0, "18")
    # app.mainloop()

