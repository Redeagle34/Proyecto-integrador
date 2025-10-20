import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import pandas as pd
import sys
from io import StringIO
from src.charts import heatmap_IMC_vs_sueño, scatter_IMC_vs_sueño, steps_sleep_chart, sleep_quality_vs_age, bar_avg_by_group, scatter_IMC_vs_calidad_sueño
from src.reports import sleep_vs_age_report, sleep_vs_physical_activity_report, gender_vs_stress_level, BMI_vs_sleep_duration, BMI_vs_sleep_quality, steps_vs_sleep_quality
from src.aws import getCSVfromAWS

class GraphSelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis de Sueño - Gráficas y Reportes")
        self.geometry("800x600")
        self.minsize(1080, 720)
        self.data = None
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="Análisis de Datos de Sueño", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Frame para cargar datos
        load_frame = ttk.LabelFrame(main_frame, text="Cargar Datos", padding=10)
        load_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_label = ttk.Label(load_frame, text="No hay datos cargados", 
                                    foreground="red")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # Contenedor para botones de carga
        btn_container = ttk.Frame(load_frame)
        btn_container.pack(side=tk.RIGHT, padx=5)
        
        btn_load_aws = ttk.Button(btn_container, text="🌐 Cargar desde AWS", 
                                 command=self.load_data_from_aws)
        btn_load_aws.pack(side=tk.LEFT, padx=5)
        
        btn_load = ttk.Button(btn_container, text="📁 Cargar CSV/Excel Local", 
                             command=self.load_data)
        btn_load.pack(side=tk.LEFT, padx=5)
        
        # Notebook (pestañas) para Gráficas y Reportes
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Pestaña de Gráficas
        self.create_graphs_tab()
        
        # Pestaña de Reportes
        self.create_reports_tab()
        
        # Botones inferiores
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        btn_exit = ttk.Button(btn_frame, text="Salir", command=self.quit)
        btn_exit.pack(side=tk.LEFT, padx=5)
        
        # Barra de estado
        self.status = tk.StringVar(value="Listo. Cargue los datos para comenzar.")
        statusbar = ttk.Label(self, textvariable=self.status, 
                             relief=tk.SUNKEN, anchor=tk.W, padding=(4,2))
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_graphs_tab(self):
        """Crear pestaña de gráficas"""
        graph_tab = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(graph_tab, text="Gráficas")
        
        # Frame para seleccionar gráfica
        graph_frame = ttk.LabelFrame(graph_tab, text="Seleccionar Gráfica", padding=15)
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

        rb4 = ttk.Radiobutton(graph_frame, 
                             text="Gráfica de Barras - Calidad del Sueño vs Edad",
                             variable=self.graph_choice, 
                             value="sleep_quality_age")
        rb4.pack(anchor=tk.W, pady=8)

        rb5 = ttk.Radiobutton(graph_frame, 
                             text="Gráfica de Barras - Estrés por Género",
                             variable=self.graph_choice, 
                             value="stress_by_gender")
        rb5.pack(anchor=tk.W, pady=8)
        
        rb6 = ttk.Radiobutton(graph_frame, 
                             text="Scatter Plot - IMC vs Calidad del Sueño",
                             variable=self.graph_choice, 
                             value="scatter_imc_calidad")
        rb6.pack(anchor=tk.W, pady=8)

        
        # Botón para mostrar gráfica
        btn_frame = ttk.Frame(graph_tab)
        btn_frame.pack(pady=20)
        
        self.btn_show_graph = ttk.Button(btn_frame, text="Mostrar Gráfica", 
                                   command=self.show_graph, 
                                   state=tk.DISABLED)
        self.btn_show_graph.pack(side=tk.LEFT, padx=5)
    
    def create_reports_tab(self):
        """Crear pestaña de reportes"""
        report_tab = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(report_tab, text="📄 Reportes")
        
        # Frame izquierdo - Selección de reporte
        left_frame = ttk.Frame(report_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        select_frame = ttk.LabelFrame(left_frame, text="Seleccionar Reporte", padding=15)
        select_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variable para radio buttons de reportes
        self.report_choice = tk.StringVar(value="sleep_age")
        
        # Radio buttons para cada reporte
        rb1 = ttk.Radiobutton(select_frame, 
                             text="Calidad de Sueño\nvs Edad",
                             variable=self.report_choice, 
                             value="sleep_age")
        rb1.pack(anchor=tk.W, pady=8)
        
        rb2 = ttk.Radiobutton(select_frame, 
                             text="Calidad de Sueño\nvs Actividad Física",
                             variable=self.report_choice, 
                             value="sleep_physical")
        rb2.pack(anchor=tk.W, pady=8)
        
        rb3 = ttk.Radiobutton(select_frame, 
                             text="Nivel de Estrés\nvs Género",
                             variable=self.report_choice, 
                             value="gender_stress")
        rb3.pack(anchor=tk.W, pady=8)

        rb4 = ttk.Radiobutton(select_frame, 
                             text="IMC\nvs Duración de Sueño",
                             variable=self.report_choice, 
                             value="IMC_sleepduration")
        rb4.pack(anchor=tk.W, pady=8)
        
        rb5 = ttk.Radiobutton(select_frame, 
                             text="IMC\nvs Calidad de Sueño",
                             variable=self.report_choice, 
                             value="IMC_sleepquality")
        rb5.pack(anchor=tk.W, pady=8)

        rb6 = ttk.Radiobutton(select_frame, 
                            text="Pasos Diarios\nvs Calidad del Sueño", 
                            variable=self.report_choice, 
                            value="steps_sleepquality")
        rb6.pack(anchor=tk.W, pady=8)

        

        # Botón para generar reporte
        btn_frame = ttk.Frame(select_frame)
        btn_frame.pack(pady=20)
        
        self.btn_generate_report = ttk.Button(btn_frame, text="Generar Reporte", 
                                   command=self.show_report, 
                                   state=tk.DISABLED)
        self.btn_generate_report.pack(padx=5)
        
        # Frame derecho - Área de visualización del reporte
        right_frame = ttk.Frame(report_tab)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        output_frame = ttk.LabelFrame(right_frame, text="Resultado del Reporte", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto con scroll para mostrar el reporte
        self.report_output = scrolledtext.ScrolledText(output_frame, 
                                                       wrap=tk.WORD, 
                                                       width=50, 
                                                       height=20,
                                                       font=("Courier", 10))
        self.report_output.pack(fill=tk.BOTH, expand=True)
        
        # Botón para limpiar
        btn_clear = ttk.Button(right_frame, text="Limpiar", 
                              command=lambda: self.report_output.delete(1.0, tk.END))
        btn_clear.pack(pady=5)
    
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
                self.btn_show_graph.config(state=tk.NORMAL)
                self.btn_generate_report.config(state=tk.NORMAL)
                self.status.set(f"Datos cargados: {len(self.data)} registros")
                messagebox.showinfo("Éxito", f"Datos cargados correctamente\nRegistros: {len(self.data)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
                self.status.set("Error al cargar datos")
    
    def load_data_from_aws(self):
        """Cargar datos desde AWS S3"""
        try:
            # Mostrar mensaje de carga
            self.status.set("Conectando a AWS S3...")
            self.update_idletasks()  # Actualizar la interfaz
            
            # Cargar datos desde AWS
            self.data = getCSVfromAWS()
            
            # Actualizar la interfaz
            self.file_label.config(text=f"✓ Datos cargados desde AWS S3", 
                                  foreground="green")
            self.btn_show_graph.config(state=tk.NORMAL)
            self.btn_generate_report.config(state=tk.NORMAL)
            self.status.set(f"Datos cargados desde AWS: {len(self.data)} registros")
            messagebox.showinfo("Éxito", 
                              f"Datos cargados correctamente desde AWS S3\n"
                              f"Registros: {len(self.data)}\n"
                              f"Columnas: {len(self.data.columns)}")
            
        except ValueError as ve:
            # Error de credenciales
            messagebox.showerror("Error de Configuración", 
                               f"No se pudieron cargar las credenciales AWS:\n\n{str(ve)}\n\n"
                               f"Asegúrate de tener un archivo .env con:\n"
                               f"AWS_ACCESS_KEY_ID=tu_clave\n"
                               f"AWS_SECRET_ACCESS_KEY=tu_secreto\n"
                               f"AWS_REGION=us-west-1")
            self.status.set("Error: Credenciales AWS no configuradas")
            
        except Exception as e:
            # Otros errores
            messagebox.showerror("Error", 
                               f"No se pudieron cargar los datos desde AWS:\n\n{str(e)}")
            self.status.set("Error al cargar datos desde AWS")
    
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

            elif choice == "sleep_quality_age":
                self.status.set("Mostrando: Calidad del Sueño vs Edad")
                sleep_quality_vs_age(self.data)

            elif choice == "stress_by_gender":
                self.status.set("Mostrando: Estrés por Género")
                bar_avg_by_group(self.data,"Gender","Stress Level")
            
            elif choice == "scatter_imc_calidad":
                self.status.set("Mostrando: Scatter Plot IMC vs Calidad del Sueño (Santiago)")
                scatter_IMC_vs_calidad_sueño(self.data)
            
            elif choice == 'steps':
                self.status.set("Mostrando: Pasos Diarios vs Calidad del Sueño")
                steps_sleep_chart(self.data)

        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la gráfica:\n{str(e)}")
            self.status.set("Error al mostrar gráfica")
    
    def show_report(self):
        """Mostrar el reporte seleccionado"""
        if self.data is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar los datos")
            return
        
        choice = self.report_choice.get()
        
        # Limpiar el área de texto
        self.report_output.delete(1.0, tk.END)
        
        # Capturar la salida de print
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            if choice == "sleep_age":
                self.status.set("Generando: Reporte Calidad de Sueño vs Edad")
                sleep_vs_age_report(self.data)
                
            elif choice == "sleep_physical":
                self.status.set("Generando: Reporte Calidad de Sueño vs Actividad Física")
                sleep_vs_physical_activity_report(self.data)
            
            elif choice == "gender_stress":
                self.status.set("Generando: Reporte Nivel de Estrés vs Género")
                gender_vs_stress_level(self.data)
            
            elif choice == "IMC_sleepduration":
                self.status.set("Generando: Reporte IMC vs Duración de Sueño")
                BMI_vs_sleep_duration(self.data)
            
            elif choice == "IMC_sleepquality":
                self.status.set("Generando: Reporte IMC vs Calidad de Sueño")
                BMI_vs_sleep_quality(self.data)

            elif choice == "steps_sleepquality":
                self.status.set("Generando: Reporte Pasos Diarios vs Calidad de Sueño")
                steps_vs_sleep_quality(self.data)

            
            # Obtener la salida capturada
            output = sys.stdout.getvalue()
            
            # Mostrar en el área de texto
            self.report_output.insert(tk.END, output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte:\n{str(e)}")
            self.status.set("Error al generar reporte")
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout

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

