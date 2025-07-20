import customtkinter as ctk
import tkinter.messagebox as tkmb
from subventanas import centrar_ventana, ToplevelWindowDuenio, ToplevelWindowMascotaPerdida, ToplevelWindowEventoPerdida, ToplevelWindowMascotaEncontrada, ToplevelWindowPersona, ToplevelWindowEventoEncuentro, ToplevelWindowBuscarEncontradas, ToplevelWindowBuscarPerdidas, ToplevelWindowReporte
from funciones import guardar_reporte_encuentro, guardar_reporte_perdida
#listas temporales donde se guardan los datos ingresados por el usuario
reportes_perdidas = []
reportes_encontradas= []

#---------------Ventana Mascotas Perdidas----------------------------
class ToplevelWindowPerdida(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("Mascota Perdida")

        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        self.datos_perdida = {
            "persona": None,
            "mascota": None,
            "evento": None
        }

        self.label = ctk.CTkLabel(self, text="Reporte Mascota Perdida.")
        self.label.pack(pady=10)
        
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.button_datos_duenio = ctk.CTkButton(
            form_frame, text="Datos dueño", command=self.open_toplevel_persona, height=40, width=200)
        self.button_datos_duenio.pack(pady=10)

        self.button_datos_mascota = ctk.CTkButton(
            form_frame, text="Datos Mascota", command=self.open_toplevel_mascota_encontrada, height=40, width=200)
        self.button_datos_mascota.pack(pady=10)

        self.button_evento_perdida = ctk.CTkButton(
            form_frame, text="Lugar y fecha", command=self.open_toplevel_evento_encuentro, height=40, width=200)
        self.button_evento_perdida.pack(pady=10)

        self.button_guardar = ctk.CTkButton(
            form_frame, text="Guardar", fg_color="dark blue", hover_color="blue",
            command=self.guardar_datos, height=40, width=200)
        self.button_guardar.pack(pady=10)

        # Inicializamos atributos para las subventanas
        self.toplevel_window_persona = None
        self.toplevel_window_mascota_encontrada = None
        self.toplevel_window_evento_encuentro = None
        self.toplevel_window_reporte = None

        centrar_ventana(self, 400, 400, 25)

    def recibir_datos_persona(self, datos):
        self.datos_perdida["persona"] = datos
    
    def recibir_datos_mascota(self, datos):
        self.datos_perdida["mascota"] = datos

    def recibir_datos_evento(self, datos):
        self.datos_perdida["evento"] = datos


    def guardar_datos(self):
        campos_faltantes = []

        if not self.datos_perdida["persona"]:
            campos_faltantes.append("Datos del dueño")
        if not self.datos_perdida["mascota"]:
            campos_faltantes.append("Datos de la mascota")
        if not self.datos_perdida["evento"]:
            campos_faltantes.append("Fecha y lugar")

        if campos_faltantes:
            mensaje = "Faltan completar los siguientes campos:\n\n" + "\n".join(f"- {campo}" for campo in campos_faltantes)
            tkmb.showwarning("Datos incompletos", mensaje)
            return

        # Si está todo ok, armamos el texto
        p = self.datos_perdida["persona"]
        m = self.datos_perdida["mascota"]
        e = self.datos_perdida["evento"]

        texto = f"""
    🐾 Reporte de pérdida:
    📅 Fecha: {e.get("fecha", "—")}
    📍 Lugar: {e.get("lugar", "—")}

    🐶 Mascota:
    - Nombre: {m.get("nombre", "—")}
    - Tipo: {m.get("tipo", "—")}
    - Edad: {m.get("edad", "—")}
    - Color: {m.get("color", "—")}
    - Sexo: {m.get("sexo", "—")}
    """
        if "raza" in m:
            texto += f"- Raza: {m['raza']}\n"
        if "tamano" in m:
            texto += f"- Tamaño: {m['tamano']}\n"
        if "subtipo" in m:
            texto += f"- Tipo específico: {m['subtipo']}\n"

        texto += f"""
    👤 Dueño:
    - Nombre: {p.get("nombre", "—")}
    - Teléfono: {p.get("telefono", "—")}
    """

        # Mostrar reporte en ventana nueva
        ventana = ToplevelWindowReporte(self.datos_perdida.copy(), "perdida", texto)
        
        self.after(100, self.destroy)

    def open_toplevel_persona(self):
        if self.toplevel_window_persona is None or not self.toplevel_window_persona.winfo_exists():
            self.toplevel_window_persona = ToplevelWindowDuenio(self)
        else:
            self.toplevel_window_persona.focus()

    def open_toplevel_mascota_encontrada(self):
        if self.toplevel_window_mascota_encontrada is None or not self.toplevel_window_mascota_encontrada.winfo_exists():
            self.toplevel_window_mascota_encontrada = ToplevelWindowMascotaPerdida(self)
        else:
            self.toplevel_window_mascota_encontrada.focus()

    def open_toplevel_evento_encuentro(self):
        if self.toplevel_window_evento_encuentro is None or not self.toplevel_window_evento_encuentro.winfo_exists():
            self.toplevel_window_evento_encuentro = ToplevelWindowEventoPerdida(self)
        else:
            self.toplevel_window_evento_encuentro.focus()


#----------------------Ventana Mascotas Encontradas-----------------------
class ToplevelWindowEncontrada(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("Mascota Encontrada")

        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        self.datos_encuentro = {
            "persona": None,
            "mascota": None,
            "evento": None
        }

        # Frame principal para el formulario
        self.label = ctk.CTkLabel(self, text="Reporte Mascota Encontrada.")
        self.label.pack(pady=10)
        
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.button_datos_persona = ctk.CTkButton(form_frame, text="Datos persona", command=self.open_toplevel_persona, height=40, width=200)
        self.button_datos_persona.pack(pady=10)

        self.button_datos_mascota = ctk.CTkButton(form_frame, text="Datos Mascota", command=self.open_toplevel_mascota_encontrada, height=40, width=200)
        self.button_datos_mascota.pack(pady=10)

        self.button_evento_encuentro = ctk.CTkButton(form_frame, text="Lugar y fecha", command=self.open_toplevel_evento_encuentro, height=40, width=200)
        self.button_evento_encuentro.pack(pady=10)

        self.button_guardar = ctk.CTkButton(form_frame, text="Guardar", fg_color="dark blue", hover_color="blue", command=self.guardar_datos, height=40, width=200)
        self.button_guardar.pack(pady=10)
        
        self.toplevel_window_persona = None
        self.toplevel_window_mascota_encontrada = None
        self.toplevel_window_evento_encuentro = None
        
        centrar_ventana(self, 400, 400, 25)

    def recibir_datos_persona(self, datos):
        self.datos_encuentro["persona"] = datos
    
    def recibir_datos_mascota(self, datos):
        self.datos_encuentro["mascota"] = datos

    def recibir_datos_evento(self, datos):
        self.datos_encuentro["evento"] = datos


    def guardar_datos(self):
        campos_faltantes = []

        if not self.datos_encuentro["persona"]:
            campos_faltantes.append("Datos del dueño")
        if not self.datos_encuentro["mascota"]:
            campos_faltantes.append("Datos de la mascota")
        if not self.datos_encuentro["evento"]:
            campos_faltantes.append("Fecha y lugar")

        if campos_faltantes:
            mensaje = "Faltan completar los siguientes campos:\n\n" + "\n".join(f"- {campo}" for campo in campos_faltantes)
            tkmb.showwarning("Datos incompletos", mensaje)
            return

    # Si está todo ok, armamos el texto
        p = self.datos_encuentro["persona"]
        m = self.datos_encuentro["mascota"]
        e = self.datos_encuentro["evento"]

        texto = f"""
       🐾 Reporte de encuentro:
        📅 Fecha: {e.get("fecha", "—")}
        📍 Lugar: {e.get("lugar", "—")}

        🐶 Mascota:\n"""

        if m.get("tiene_chapa") == "Sí" and m.get("nombre"):
              texto += f"- Nombre: {m['nombre']}\n"

        texto += f"""
        - Tipo: {m['tipo']}
        - Color: {m['color']}
        - Sexo: {m['sexo']}
         """

        if "raza" in m:
             texto += f"- Raza: {m['raza']}\n"
        if "tamano" in m:
            texto += f"- Tamaño: {m['tamano']}\n"
        if "subtipo" in m:
            texto += f"- Tipo específico: {m['subtipo']}\n"
                    
        texto += f"""
        👤 Dueño:
        - Nombre: {p.get("nombre", "—")}
        - Teléfono: {p.get("telefono", "—")}
        """

        # Mostrar reporte en ventana nueva
        ventana = ToplevelWindowReporte(self.datos_encuentro.copy(), "encuentro", texto)
        self.after(100, self.destroy)

    def open_toplevel_persona(self):
        if self.toplevel_window_persona is None or not self.toplevel_window_persona.winfo_exists():
            self.toplevel_window_persona = ToplevelWindowPersona(self)
        else:
            self.toplevel_window_persona.focus()

    def open_toplevel_mascota_encontrada(self):
        if self.toplevel_window_mascota_encontrada is None or not self.toplevel_window_mascota_encontrada.winfo_exists():
            self.toplevel_window_mascota_encontrada = ToplevelWindowMascotaEncontrada(self)
        else:
            self.toplevel_window_mascota_encontrada.focus()

    def open_toplevel_evento_encuentro(self):
        if self.toplevel_window_evento_encuentro is None or not self.toplevel_window_evento_encuentro.winfo_exists():
            self.toplevel_window_evento_encuentro = ToplevelWindowEventoEncuentro(self)
        else:
            self.toplevel_window_evento_encuentro.focus()

#----------------------Ventana Busqueda-----------------------
class ToplevelWindowBusqueda(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("Búsqueda Mascotas")

        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        self.toplevel_window_busqueda_perdidas = None
        self.toplevel_window_busqueda_encontradas = None


        # Frame principal para el formulario
        self.label = ctk.CTkLabel(self, text="Buscar entre mascotas perdidas y encontradas.")
        self.label.pack(pady=10)
        
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.button_buscar_perdidas = ctk.CTkButton(form_frame, text="Buscar Mascotas Perdidas", command=self.open_toplevel_busqueda_perdidas, height=40, width=200)
        self.button_buscar_perdidas.pack(pady=10)

        self.button_buscar_encontradas = ctk.CTkButton(form_frame, text="Buscar Mascotas encontradas", command=self.open_toplevel_busqueda_encontradas, height=40, width=200)
        self.button_buscar_encontradas.pack(pady=10)

        self.toplevel_window_busqueda_perdidas = None
        self.toplevel_window_busqueda_encontradas = None
                
        centrar_ventana(self, 400, 400, 25)

    def open_toplevel_busqueda_perdidas(self):
           if self.toplevel_window_busqueda_perdidas is None or not self.toplevel_window_busqueda_perdidas.winfo_exists():
               self.toplevel_window_busqueda_perdidas = ToplevelWindowBuscarPerdidas(self)
           else:
               self.toplevel_window_busqueda_perdidas.focus()

    def open_toplevel_busqueda_encontradas(self):
           if self.toplevel_window_busqueda_encontradas is None or not self.toplevel_window_busqueda_encontradas.winfo_exists():
               self.toplevel_window_busqueda_encontradas = ToplevelWindowBuscarEncontradas(self)
           else:
               self.toplevel_window_busqueda_encontradas.focus()