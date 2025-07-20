import customtkinter as ctk
import re
import datetime
import tkinter.messagebox as tkmb
from mapa import generar_mapa, direccion_valida
from funciones import guardar_reporte_encuentro, guardar_reporte_perdida, filtrar_reportes, obtener_reportes_encuentro, obtener_reportes_perdida

def centrar_ventana(ventana, ancho, alto, margen_superior=0):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 4 + margen_superior
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


#================Subventanas Mascota Perdida =======================
#---------------Datos dueño-----------------------------
class ToplevelWindowDuenio(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("Datos dueño")
        self.parent = parent

        self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 1. Nombre del dueño
        ctk.CTkLabel(form_frame, text="Nombre del dueño:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_nombreDuenio = ctk.CTkEntry(form_frame, placeholder_text="Ej: Juan Pérez", width=300, height=35, font=("Arial", 12))
        self.entry_nombreDuenio.pack(pady=(0, 15))

        # 2. Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono de contacto:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_telefonoDuenio = ctk.CTkEntry(form_frame, placeholder_text="Ej: 54 11 1234-5678", width=300, height=35)
        self.entry_telefonoDuenio.pack(pady=(0, 20))

        self.button_confirmar_duenio = ctk.CTkButton(form_frame, text="Confirmar", command=lambda:confirmar_datos(self) ,height=40, width=200)
        self.button_confirmar_duenio.pack(pady=10)

        def confirmar_datos(self):
            telefono_ingresado = self.entry_telefonoDuenio.get()

            solo_digitos = re.sub(r"\D", "", telefono_ingresado)

            if not (8 <= len(solo_digitos) <= 15):
                tkmb.showinfo("Error", "El número de teléfono debe tener entre 8 y 15 dígitos.")
                return  # No continúa si no pasa la validación

            datos = {
            "nombre": self.entry_nombreDuenio.get(),
            "telefono": self.entry_telefonoDuenio.get()
        }
            self.parent.recibir_datos_persona(datos)
            self.destroy()  # Esto cierra la ventana

        centrar_ventana(self, 400, 400, 25)


#-----------------------Datos Mascota Perdida ------------------------
class ToplevelWindowMascotaPerdida(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x600")
        self.title("Datos Mascota")
        self.parent = parent

        self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

                # Frame principal de la ventana
        frame_total = ctk.CTkFrame(self, fg_color="transparent")
        frame_total.pack(expand=True, fill="both", padx=20, pady=20)

        # Formulario arriba
        form_frame = ctk.CTkFrame(frame_total, fg_color="transparent")
        form_frame.pack(fill="x", expand=False, pady=(0, 10))


        # Botón abajo
        boton_confirmar = ctk.CTkButton(frame_total, text="Confirmar", command=lambda:confirmar_datos(self), height=30, width=200)
        boton_confirmar.pack(side="bottom", pady=10)


        # 3. Nombre mascota
        ctk.CTkLabel(form_frame, text="Nombre de la mascota:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_nombreMascotaPerdida = ctk.CTkEntry(form_frame, placeholder_text="Ej: Pompón", width=250, height=25, font=("Arial", 12))
        self.entry_nombreMascotaPerdida.pack(pady=(0, 10))

        # 4. Edad mascota
        ctk.CTkLabel(form_frame, text="Edad:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_edadMascota = ctk.CTkEntry(form_frame, placeholder_text="Ej: 10", width=250, height=25, font=("Arial", 12))
        self.entry_edadMascota.pack(pady=(0, 10))

        # 5. Color mascota
        ctk.CTkLabel(form_frame, text="Color:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_colorMascotaPerdida = ctk.CTkEntry(form_frame, placeholder_text="Ej: Negro", width=250, height=25, font=("Arial", 12))
        self.entry_colorMascotaPerdida.pack(pady=(0, 10))

        # 6. Sexo mascota
        sexo_var = ctk.StringVar(value="F")

        # Frame para alinear horizontalmente
        frame_sexo = ctk.CTkFrame(form_frame, fg_color="transparent")
        frame_sexo.pack(pady=(10, 15))

        ctk.CTkRadioButton(frame_sexo, text="Femenino", variable=sexo_var, value="F").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_sexo, text="Masculino", variable=sexo_var, value="M").pack(side="left", padx=10)


        # 7. Tipo de mascota
        ctk.CTkLabel(form_frame, text="Tipo de mascota:", font=("Arial", 12), ).pack(pady=(0, 5))

        # --- Campos dinámicos ---
        self.label_raza = ctk.CTkLabel(form_frame, text="Raza:", font=("Arial", 12))
        self.entry_raza = ctk.CTkEntry(form_frame, placeholder_text="Ej: Labrador", width=250, height=25, font=("Arial", 12))

        self.label_tamano_perro = ctk.CTkLabel(form_frame, text="Tamaño:", font=("Arial", 12))
        self.combobox_tamano_perro = ctk.CTkComboBox(form_frame, values=["Chico", "Mediano", "Grande"], width=250, height=25, font=("Arial", 12))

        self.label_tamano_gato = ctk.CTkLabel(form_frame, text="Tamaño:", font=("Arial", 12))
        self.combobox_tamano_gato = ctk.CTkComboBox(form_frame, values=["Chico", "Mediano", "Grande"], width=250, height=25, font=("Arial", 12))

        self.label_tipo_roedor = ctk.CTkLabel(form_frame, text="Tipo:", font=("Arial", 12))
        self.combobox_tipo_roedor = ctk.CTkComboBox(form_frame, values=["Conejo", "Hámster", "Cobayo"], width=250, height=25, font=("Arial", 12))

        def ocultar_campos_dinamicos():
            self.label_raza.pack_forget()
            self.entry_raza.pack_forget()
            self.label_tamano_perro.pack_forget()
            self.combobox_tamano_perro.pack_forget()
            self.label_tamano_gato.pack_forget()
            self.combobox_tamano_gato.pack_forget()
            self.label_tipo_roedor.pack_forget()
            self.combobox_tipo_roedor.pack_forget()

        def combobox_callback(choice):
            ocultar_campos_dinamicos()
            if choice == "Perro":
                self.label_raza.pack(pady=(10, 5))
                self.entry_raza.pack(pady=(0, 10))
                self.label_tamano_perro.pack(pady=(10, 5))
                self.combobox_tamano_perro.pack(pady=(0, 15))
            elif choice == "Gato":
                self.label_tamano_gato.pack(pady=(10, 5))
                self.combobox_tamano_gato.pack(pady=(0, 15))
            elif choice == "Roedor":
                self.label_tipo_roedor.pack(pady=(10, 5))
                self.combobox_tipo_roedor.pack(pady=(0, 15))

        self.combobox_tipo = ctk.CTkComboBox(
            form_frame,
            values=["","Perro", "Gato", "Roedor"],
            width=250,
            height=25,
            font=("Arial", 12),
            command=combobox_callback
        )
        self.combobox_tipo.pack(pady=(0, 15))

        
        def confirmar_datos(self):
            tipo = self.combobox_tipo.get()
            datos = {
                "nombre": self.entry_nombreMascotaPerdida.get(),
                "edad": self.entry_edadMascota.get(),
                "color": self.entry_colorMascotaPerdida.get(),
                "sexo": sexo_var.get(),
                "tipo": tipo
            }

            # Campos condicionales según el tipo
            if tipo == "Perro":
                datos["raza"] = self.entry_raza.get()
                datos["tamano"] = self.combobox_tamano_perro.get()
            elif tipo == "Gato":
                datos["tamano"] = self.combobox_tamano_gato.get()
            elif tipo == "Roedor":
                datos["subtipo"] = self.combobox_tipo_roedor.get()

            self.parent.recibir_datos_mascota(datos)
            self.destroy()

        centrar_ventana(self, 400, 600, 25)


#------------------Evento Pérdida----------------------
class ToplevelWindowEventoPerdida(ctk.CTkToplevel):
    def __init__(self, parent,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("Evento.")
        self.parent = parent

        self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.label = ctk.CTkLabel(form_frame, text="Ingrese fecha y lugar donde fue vista por última vez." , font=("Arial", 14))
        self.label.pack(pady=(0, 15))


        # Fecha
        ctk.CTkLabel(form_frame, text="Fecha (formato DD/MM/AAAA):", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_fecha_perdida = ctk.CTkEntry(form_frame, placeholder_text="Ej: 10/04/2004", width=300, height=35, font=("Arial", 12))
        self.entry_fecha_perdida.pack(pady=(0, 15))

        # Lugar
        ctk.CTkLabel(form_frame, text="Dirección aproximada:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_lugar_perdida = ctk.CTkEntry(form_frame, placeholder_text="Ej: Calle 123, Localidad, Prov, País", width=300, height=35)
        self.entry_lugar_perdida.pack(pady=(0, 20))

        self.boton_mapa = ctk.CTkButton(form_frame, text="Ver en mapa", command=lambda:ver_mapa(self))
        self.boton_mapa.pack(pady=10)

        self.label_resultado = ctk.CTkLabel(self, text="", text_color="white")
        self.label_resultado.pack(pady=10)

        self.button_confirmar_ev_per = ctk.CTkButton(form_frame, text="Confirmar",command=lambda:confirmar_datos(self), height=40, width=200)
        self.button_confirmar_ev_per.pack(pady=10)

        def confirmar_datos(self):
            fecha_ingresada = self.entry_fecha_perdida.get().strip()
            direccion_ingresada = self.entry_lugar_perdida.get().strip()

            try:
                fecha_obj = datetime.datetime.strptime(fecha_ingresada, "%d/%m/%Y")
            except ValueError:
                tkmb.showwarning("Error", "La fecha debe tener el formato DD/MM/AAAA y ser válida.")
                return
            
            if not direccion_ingresada:
                tkmb.showwarning("Error", "La dirección no puede estar vacía.")
                return
        
            if not direccion_valida(direccion_ingresada):
                tkmb.showwarning("Error", "La dirección ingresada no es válida.")
                return

            datos = {
                "fecha": self.entry_fecha_perdida.get(),
                "lugar": self.entry_lugar_perdida.get()
            }

            self.parent.recibir_datos_evento(datos)
            self.destroy()

        centrar_ventana(self, 500, 400, 25)
        
        def ver_mapa(self):
            direccion = self.entry_lugar_perdida.get()
            if direccion.strip():
                generar_mapa(direccion)
            else:
                self.label_resultado.configure(text="Por favor ingresá una dirección.")




#================Subventanas Mascota Encontrada =======================
#---------------Datos Persona-----------------------------
class ToplevelWindowPersona(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.title("Datos Persona")
        self.parent = parent

        self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 1. Nombre persona
        ctk.CTkLabel(form_frame, text="Nombre de la persona:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_nombrePersona = ctk.CTkEntry(form_frame, placeholder_text="Ej: Juan Pérez", width=300, height=35, font=("Arial", 12))
        self.entry_nombrePersona.pack(pady=(0, 15))

        # 2. Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono de contacto:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_telefonoPersona = ctk.CTkEntry(form_frame, placeholder_text="Ej: +54 11 1234-5678", width=300, height=35)
        self.entry_telefonoPersona.pack(pady=(0, 20))

        self.button_confirmar_persona = ctk.CTkButton(form_frame, text="Confirmar", command=lambda:confirmar_datos(self),  height=40, width=200)
        self.button_confirmar_persona.pack(pady=10)

        def confirmar_datos(self):

            telefono_ingresado = self.entry_telefonoPersona.get()

            solo_digitos = re.sub(r"\D", "", telefono_ingresado)

            if not (8 <= len(solo_digitos) <= 15):
                tkmb.showinfo("Error", "El número de teléfono debe tener entre 8 y 15 dígitos.")
                return  # No continúa si no pasa la validación
            
            datos = {
            "nombre": self.entry_nombrePersona.get(),
            "telefono": self.entry_telefonoPersona.get()
        }
            self.parent.recibir_datos_persona(datos)
            self.destroy()  # Esto cierra la ventana

        centrar_ventana(self, 400, 400, 25)


#-----------------------Datos Mascota Encontrada ------------------------
class ToplevelWindowMascotaEncontrada(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.geometry("400x600")
        self.title("Datos Mascota")

        self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        centrar_ventana(self, 400, 600, 25)

        # Frame principal de la ventana
        frame_total = ctk.CTkFrame(self, fg_color="transparent")
        frame_total.pack(expand=True, fill="both", padx=20, pady=20)

        # Formulario arriba
        form_frame = ctk.CTkFrame(frame_total, fg_color="transparent")
        form_frame.pack(fill="x", expand=False, pady=(0, 10))


        # Botón abajo
        boton_confirmar = ctk.CTkButton(frame_total, text="Confirmar", command=self.confirmar_datos,  height=30, width=150)
        boton_confirmar.pack(side="bottom", pady=10)

        # Nombre mascota
        ctk.CTkLabel(form_frame, text="¿Tiene chapa identificatoria?", font=("Arial", 12)).pack(pady=(0, 5))

        self.combobox_chapa = ctk.CTkComboBox(
            form_frame,
            values=[ "No","Sí"],
            width=250,
            height=25,
            font=("Arial", 12),
            command=self.chapa_callback
        )
        self.combobox_chapa.pack(pady=(0, 10))

        # Ancla invisible para insertar debajo
        self.ancla_nombre = ctk.CTkLabel(form_frame, text="")  # No visible
        self.ancla_nombre.pack()

        # Campo del nombre (visible solo si elige "Sí")
        self.label_nombre = ctk.CTkLabel(form_frame, text="Nombre de la mascota:", font=("Arial", 12))
        self.entry_nombreMascotaPerdida = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ej: Pompón",
            width=250,
            height=25,
            font=("Arial", 12)
        )
      
        # Color mascota
        ctk.CTkLabel(form_frame, text="Color:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_colorMascotaEncontrada = ctk.CTkEntry(form_frame, placeholder_text="Ej: Negro", width=250, height=25, font=("Arial", 12))
        self.entry_colorMascotaEncontrada.pack(pady=(0, 5))

        # Sexo mascota
        self.sexo_var = ctk.StringVar(value="F")

        # Frame para alinear horizontalmente
        frame_sexo = ctk.CTkFrame(form_frame, fg_color="transparent")
        frame_sexo.pack(pady=(10, 15))

        ctk.CTkRadioButton(frame_sexo, text="Femenino", variable=self.sexo_var, value="F").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_sexo, text="Masculino", variable=self.sexo_var, value="M").pack(side="left", padx=10)


        # Tipo de mascota
        ctk.CTkLabel(form_frame, text="Tipo de mascota:", font=("Arial", 12), ).pack(pady=(0, 5))

        # --- Campos dinámicos ---
        self.label_raza = ctk.CTkLabel(form_frame, text="Raza:", font=("Arial", 12))
        self.entry_raza = ctk.CTkEntry(form_frame, placeholder_text="Ej: Labrador", width=250, height=25, font=("Arial", 12))

        self.label_tamano_perro = ctk.CTkLabel(form_frame, text="Tamaño:", font=("Arial", 12))
        self.combobox_tamano_perro = ctk.CTkComboBox(form_frame, values=["Chico", "Mediano", "Grande"], width=250, height=25, font=("Arial", 12))

        self.label_tamano_gato = ctk.CTkLabel(form_frame, text="Tamaño:", font=("Arial", 12))
        self.combobox_tamano_gato = ctk.CTkComboBox(form_frame, values=["Chico", "Mediano", "Grande"], width=250, height=25, font=("Arial", 12))

        self.label_tipo_roedor = ctk.CTkLabel(form_frame, text="Tipo:", font=("Arial", 12))
        self.combobox_tipo_roedor = ctk.CTkComboBox(form_frame, values=["Conejo", "Hámster", "Cobayo"], width=250, height=25, font=("Arial", 12))

        def ocultar_campos_dinamicos():
            self.label_raza.pack_forget()
            self.entry_raza.pack_forget()
            self.label_tamano_perro.pack_forget()
            self.combobox_tamano_perro.pack_forget()
            self.label_tamano_gato.pack_forget()
            self.combobox_tamano_gato.pack_forget()
            self.label_tipo_roedor.pack_forget()
            self.combobox_tipo_roedor.pack_forget()

        def combobox_callback(choice):
            ocultar_campos_dinamicos()
            if choice == "Perro":
                self.label_raza.pack(pady=(10, 5))
                self.entry_raza.pack(pady=(0, 10))
                self.label_tamano_perro.pack(pady=(10, 5))
                self.combobox_tamano_perro.pack(pady=(0, 15))
            elif choice == "Gato":
                self.label_tamano_gato.pack(pady=(10, 5))
                self.combobox_tamano_gato.pack(pady=(0, 15))
            elif choice == "Roedor":
                self.label_tipo_roedor.pack(pady=(10, 5))
                self.combobox_tipo_roedor.pack(pady=(0, 15))

        self.combobox_tipo = ctk.CTkComboBox(
            form_frame,
            values=["","Perro", "Gato", "Roedor"],
            width=250,
            height=25,
            font=("Arial", 12),
            command=combobox_callback
        )
        self.combobox_tipo.pack(pady=(0, 15))

        import tkinter.messagebox as tkmb

    def confirmar_datos(self):
        tiene_chapa = self.combobox_chapa.get()
        nombre = self.entry_nombreMascotaPerdida.get().strip() if tiene_chapa == "Sí" else ""
        color = self.entry_colorMascotaEncontrada.get().strip()
        sexo = self.sexo_var.get()
        tipo = self.combobox_tipo.get()

        campos_obligatorios = []

        if not color:
            campos_obligatorios.append("Color")
        if not tipo:
            campos_obligatorios.append("Tipo de mascota")

        # Condicionales según tipo
        if tipo == "Perro":
            raza = self.entry_raza.get().strip()
            tamano = self.combobox_tamano_perro.get()
            if not raza:
                campos_obligatorios.append("Raza")
            if not tamano:
                campos_obligatorios.append("Tamaño (perro)")
        elif tipo == "Gato":
            tamano = self.combobox_tamano_gato.get()
            if not tamano:
                campos_obligatorios.append("Tamaño (gato)")
        elif tipo == "Roedor":
            subtipo = self.combobox_tipo_roedor.get()
            if not subtipo:
                campos_obligatorios.append("Tipo de roedor")

        if campos_obligatorios:
            mensaje = "Faltan completar los siguientes campos:\n\n" + "\n".join(f"- {campo}" for campo in campos_obligatorios)
            tkmb.showwarning("Datos incompletos", mensaje)
            return

        # Armar diccionario de forma condicional
        datos = {
            "tiene_chapa": tiene_chapa,
            "color": color,
            "sexo": sexo,
            "tipo": tipo
        }

        if tiene_chapa == "Sí" and nombre:
            datos["nombre"] = nombre

        if tipo == "Perro":
            datos["raza"] = raza
            datos["tamano"] = tamano
        elif tipo == "Gato":
            datos["tamano"] = tamano
        elif tipo == "Roedor":
            datos["subtipo"] = subtipo

        self.parent.recibir_datos_mascota(datos)
        self.destroy()

    def chapa_callback(self, choice):
        if choice == "Sí":
            self.label_nombre.pack(pady=(0, 5), before=self.ancla_nombre)
            self.entry_nombreMascotaPerdida.pack(pady=(0, 5), before=self.ancla_nombre)
        else:
            self.label_nombre.pack_forget()
            self.entry_nombreMascotaPerdida.pack_forget()

        centrar_ventana(self, 400, 600, 25)


#------------------Evento Encuentro----------------------
class ToplevelWindowEventoEncuentro(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")
        self.title("Evento.")
        self.parent = parent

        self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.label = ctk.CTkLabel(form_frame, text="Ingrese fecha y lugar donde fue encontrada." , font=("Arial", 14))
        self.label.pack(pady=(0, 15))


        # Fecha
        ctk.CTkLabel(form_frame, text="Fecha (formato DD/MM/AAAA):", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_fecha_encuentro = ctk.CTkEntry(form_frame, placeholder_text="Ej: 10/04/2004", width=300, height=35, font=("Arial", 12))
        self.entry_fecha_encuentro.pack(pady=(0, 15))

        # Lugar
        ctk.CTkLabel(form_frame, text="Dirección aproximada:", font=("Arial", 12)).pack(pady=(0, 5))
        self.entry_lugar_encuentro = ctk.CTkEntry(form_frame, placeholder_text="Ej: Calle 123, Localidad, Prov, País", width=300, height=35)
        self.entry_lugar_encuentro.pack(pady=(0, 20))

        self.boton_mapa = ctk.CTkButton(form_frame, text="Ver en mapa", command=lambda:ver_mapa(self))
        self.boton_mapa.pack(pady=10)

        self.label_resultado = ctk.CTkLabel(self, text="", text_color="white")
        self.label_resultado.pack(pady=10)

        self.button_confirmar_ev_enc = ctk.CTkButton(form_frame, text="Confirmar", command=lambda:confirmar_datos(self),  height=40, width=200)
        self.button_confirmar_ev_enc.pack(pady=10)

        def confirmar_datos(self):
            fecha_ingresada = self.entry_fecha_encuentro.get().strip()
            direccion_ingresada = self.entry_lugar_encuentro.get().strip()

            try:
                fecha_obj = datetime.datetime.strptime(fecha_ingresada, "%d/%m/%Y")
            except ValueError:
                tkmb.showwarning("Error", "La fecha debe tener el formato DD/MM/AAAA y ser válida.")
                return
            
            if not direccion_ingresada:
                tkmb.showwarning("Error", "La dirección no puede estar vacía.")
                return
        
            if not direccion_valida(direccion_ingresada):
                tkmb.showwarning("Error", "La dirección ingresada no es válida.")
                return

            datos = {
                "fecha": self.entry_fecha_encuentro.get(),
                "lugar": self.entry_lugar_encuentro.get()
            }

            self.parent.recibir_datos_evento(datos)
            self.destroy()
            
        centrar_ventana(self, 500, 400, 25)

        def ver_mapa(self):
            direccion = self.entry_lugar_encuentro.get()
            if direccion.strip():
                generar_mapa(direccion)
            else:
                self.label_resultado.configure(text="Por favor ingresá una dirección.")


#------------------Busqueda Perdidas----------------------
class ToplevelWindowBuscarPerdidas(ctk.CTkToplevel):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x600")
        self.title("Buscar Mascotas Perdidas.")
        centrar_ventana(self, 400, 600, 25)

        #self.transient(parent)  # La hace modal respecto al padre
        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label = ctk.CTkLabel(
            form_frame,
            text="Buscá entre las mascotas perdidas reportadas.",
            font=("Arial", 14)
        )
        self.label.pack(pady=(0, 15))

        # -------- Filtros --------
        # Tipo de mascota
        self.tipo_label = ctk.CTkLabel(form_frame, text="Tipo de mascota:")
        self.tipo_label.pack(anchor="w")
        self.combo_tipo = ctk.CTkComboBox(form_frame, values=["", "Perro", "Gato", "Roedor"])
        self.combo_tipo.pack(fill="x", pady=(0, 10))

        # Color
        self.color_label = ctk.CTkLabel(form_frame, text="Color:")
        self.color_label.pack(anchor="w")
        self.entry_color = ctk.CTkEntry(form_frame, placeholder_text="Ej: negro, blanco")
        self.entry_color.pack(fill="x", pady=(0, 10))

        # Zona
        self.zona_label = ctk.CTkLabel(form_frame, text="Zona:")
        self.zona_label.pack(anchor="w")
        self.entry_zona = ctk.CTkEntry(form_frame, placeholder_text="Ej: Palermo, Centro")
        self.entry_zona.pack(fill="x", pady=(0, 10))

        # Botón Buscar
        self.button_buscar_encontradas = ctk.CTkButton(
            form_frame,
            text="Buscar",
            command=self.confirmar_datos,
            height=40,
            width=200
        )
        self.button_buscar_encontradas.pack(pady=10)

        self.textbox_resultados = ctk.CTkTextbox(self, width=360, height=200)
        self.textbox_resultados.pack(pady=10)
        self.textbox_resultados.configure(state="disabled")

    def confirmar_datos(self):
        tipo = self.combo_tipo.get()
        color = self.entry_color.get().strip()
        zona = self.entry_zona.get().strip()

        reportes = obtener_reportes_perdida()
        resultados = filtrar_reportes(reportes, tipo or None, color or None, zona or None)

        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("0.0", "end")

        if not resultados:
            self.textbox_resultados.insert("0.0", "No se encontraron coincidencias.")
        else:
            for r in resultados:
                texto = f"""
    📅 {r.fecha.strftime('%d/%m/%Y')}
    📍 Zona: {r.lugar}
    🐶 Tipo: {r.mascota.tipo}
    🎨 Color: {r.mascota.color}
    👤 Dueño: {r.persona.nombre} - {r.persona.telefono}
    ----------------------------
    """
                self.textbox_resultados.insert("end", texto)

        self.textbox_resultados.configure(state="disabled")





#------------------Busqueda Encontradas----------------------

class ToplevelWindowBuscarEncontradas(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x600")
        self.title("Buscar Mascotas Encontradas.")
        centrar_ventana(self, 400, 600, 25)

        self.grab_set()
        self.focus_force()

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label = ctk.CTkLabel(
            form_frame,
            text="Buscá entre las mascotas encontradas reportadas.",
            font=("Arial", 14)
        )
        self.label.pack(pady=(0, 15))

        # -------- Filtros --------
        self.tipo_label = ctk.CTkLabel(form_frame, text="Tipo de mascota:")
        self.tipo_label.pack(anchor="w")
        self.combo_tipo = ctk.CTkComboBox(form_frame, values=["", "Perro", "Gato", "Roedor"])
        self.combo_tipo.pack(fill="x", pady=(0, 10))

        self.color_label = ctk.CTkLabel(form_frame, text="Color:")
        self.color_label.pack(anchor="w")
        self.entry_color = ctk.CTkEntry(form_frame, placeholder_text="Ej: negro, blanco")
        self.entry_color.pack(fill="x", pady=(0, 10))

        self.zona_label = ctk.CTkLabel(form_frame, text="Zona:")
        self.zona_label.pack(anchor="w")
        self.entry_zona = ctk.CTkEntry(form_frame, placeholder_text="Ej: Palermo, Centro")
        self.entry_zona.pack(fill="x", pady=(0, 10))

        self.button_buscar_encontradas = ctk.CTkButton(
            form_frame,
            text="Buscar",
            command=self.confirmar_datos,
            height=40,
            width=200
        )
        self.button_buscar_encontradas.pack(pady=10)

        # ✅ Textbox único, bien posicionado
        self.textbox_resultados = ctk.CTkTextbox(self, width=360, height=200, font=("Courier New", 12))
        self.textbox_resultados.pack(pady=10, expand=True, fill="both")
        self.textbox_resultados.configure(state="disabled")

    def confirmar_datos(self):
        tipo = self.combo_tipo.get()
        color = self.entry_color.get().strip()
        zona = self.entry_zona.get().strip()

        reportes = obtener_reportes_encuentro()
        resultados = filtrar_reportes(reportes, tipo or None, color or None, zona or None)

        self.textbox_resultados.configure(state="normal")
        self.textbox_resultados.delete("0.0", "end")

        if not resultados:
            self.textbox_resultados.insert("0.0", "No se encontraron coincidencias.")
        else:
            for r in resultados:
                texto = f"""
📅 {r.fecha.strftime('%d/%m/%Y')}
📍 Zona: {r.lugar}
🐶 Tipo: {r.mascota.tipo}
🎨 Color: {r.mascota.color}
👤 Reportante: {r.persona.nombre} - {r.persona.telefono}
----------------------------
"""
                self.textbox_resultados.insert("end", texto)

        self.textbox_resultados.configure(state="disabled")




        

class ToplevelWindowReporte(ctk.CTkToplevel):
    def __init__(self, datos_dict, tipo_reporte, reporte_texto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x500")
        self.datos = datos_dict
        self.tipo_reporte = tipo_reporte  # "encuentro" o "perdida"

        titulo = "Reporte de Encuentro" if tipo_reporte == "encuentro" else "Reporte de Pérdida"
        self.title(titulo)

        self.grab_set()         # Bloquea interacción con el padre
        self.focus_force()      # Fuerza el foco

        # Frame principal vertical
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(expand=True, fill="both", padx=10, pady=10)

        self.textbox = ctk.CTkTextbox(frame_principal, font=("Courier New", 13))
        self.textbox.pack(expand=True, fill="both", pady=(0, 10))
        self.textbox.insert("0.0", reporte_texto)
        self.textbox.configure(state="disabled")

        boton_confirmar = ctk.CTkButton(self, text="Confirmar y guardar", command=self.confirmar,  height=40, width=200)
        boton_confirmar.pack(pady=10)

        centrar_ventana(self, 400, 500, 25)

    def confirmar(self):
        if self.tipo_reporte == "encuentro":
             exito = guardar_reporte_encuentro(self.datos)
        else:
             exito = guardar_reporte_perdida(self.datos)

        if exito:
            tkmb.showinfo(title="Guardado", message="Reporte guardado correctamente.")
        else:
            tkmb.showinfo(title="Error", message="No se pudo guardar el reporte.")
        self.destroy()
