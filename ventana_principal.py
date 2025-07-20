import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as tkmb
from ventanas_secundarias import ToplevelWindowEncontrada, ToplevelWindowPerdida, ToplevelWindowBusqueda
from subventanas import centrar_ventana

#----------------------Ventana Principal--------------------------
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x600")
        self.title("PetMapp")

        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

        self.label = ctk.CTkLabel(frame_principal, text="Usando nuestra app podés encontrar tu mascota o ayudar a quien haya perdido la suya.", font=("Arial", 14), fg_color="transparent")
        self.label.pack(pady=10)

        self.label = ctk.CTkLabel(frame_principal, text="Elegí el reporte que querés realizar", font=("Arial", 14), fg_color="transparent")
        self.label.pack(pady=10)

        self.button_perdida = ctk.CTkButton(frame_principal, text="Mascota Perdida", command=self.open_toplevel_perdida, height=40, width=200)
        self.button_perdida.pack(pady=10)

        self.button_busqueda = ctk.CTkButton(frame_principal, text="Mascota Encontrada", command=self.open_toplevel_encontrada, height=40, width=200)
        self.button_busqueda.pack(pady=10)

        self.button_busqueda = ctk.CTkButton(frame_principal, text="Buscar Mascota", command=self.open_toplevel_busqueda, height=40, width=200)
        self.button_busqueda.pack(pady=10)

        self.toplevel_window_perdida = None
        self.toplevel_window_encontrada = None
        self.toplevel_window_busqueda = None

        # Imágenes
        frame_imagenes = ctk.CTkFrame(self)
        frame_imagenes.pack(pady=20, padx=20, fill="x", expand=True)

        imagen_pil1 = Image.open("animaless.png")
        imagen_ctk1 = ctk.CTkImage(imagen_pil1, size=(368, 246))
       
        ctk.CTkLabel(frame_imagenes, image=imagen_ctk1, text="").pack(side="left", padx=10, expand=True)
        
    def open_toplevel_perdida(self):
        if self.toplevel_window_perdida is None or not self.toplevel_window_perdida.winfo_exists():
            self.toplevel_window_perdida = ToplevelWindowPerdida(self)
        else:
            self.toplevel_window_perdida.focus()

    def open_toplevel_encontrada(self):
        if self.toplevel_window_encontrada is None or not self.toplevel_window_encontrada.winfo_exists():
            self.toplevel_window_encontrada = ToplevelWindowEncontrada(self)
        else:
            self.toplevel_window_encontrada.focus()
            
    def open_toplevel_busqueda(self):
        if self.toplevel_window_busqueda is None or not self.toplevel_window_busqueda.winfo_exists():
            self.toplevel_window_busqueda = ToplevelWindowBusqueda(self)
        else:
            self.toplevel_window_busqueda.focus()

# --- INICIO APP ---
app = App()
centrar_ventana(app, 600, 600, 50)
app.mainloop()
