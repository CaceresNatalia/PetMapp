from datetime import datetime
from abc import ABC, abstractmethod

# Clase Mascota
class Mascota:
    # Mascota: tipo, color, nombre, edad, tamaño, sexo
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str):
        self.tipo = tipo
        self.nombre = nombre
        self.color = color
        self.edad = edad
        self.tamanio = tamanio
        self.sexo = sexo

    def __str__(self):
        return f"{self.tipo} | {self.nombre} | {self.color} | Edad: {self.edad} | Tamaño: {self.tamanio} | {self.sexo}"

# Subclases específicas de Mascota
class Perro(Mascota):
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str, raza: str):
        super().__init__(tipo, nombre, color, edad, tamanio, sexo)
        self.raza = raza

    def __str__(self):
        return f"{super().__str__()} | Raza: {self.raza}"

class Gato(Mascota):
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str):
        super().__init__(tipo, nombre, color, edad, tamanio, sexo)

class Roedor(Mascota):
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str, especie: str):
        super().__init__(tipo, nombre, color, edad, tamanio, sexo)
        self.especie = especie

    def __str__(self):
        return f"{super().__str__()} | Especie: {self.especie}"

# Clase Reporte
class Reporte:
    def __init__(self, fecha: datetime, ubicacion: str, mascota: Mascota, persona: str, estado: str):
        self.fecha = fecha
        self.ubicacion = ubicacion
        self.mascota = mascota  
        self.persona = persona  
        self.estado = estado 

    def mostrar_datos(self):
        print("=== DATOS DEL REPORTE ===")
        print(f"Estado         : {self.estado}")
        print(f"Fecha          : {self.fecha.strftime('%d/%m/%Y')}")
        print(f"Ubicación      : {self.ubicacion}")
        print("Datos de la Mascota:")
        print(self.mascota)  
        print(f"Reportado por  : {self.persona}")

# Subclases específicas de Reporte
class ReportePerdida(Reporte):
    def __init__(self, fecha: datetime, ubicacion: str, mascota: Mascota, duenio_mascota: str):
        super().__init__(fecha, ubicacion, mascota, duenio_mascota, estado='Perdida')

class ReporteEncuentro(Reporte):
    def __init__(self, fecha: datetime, ubicacion: str, mascota: Mascota, encuentra_mascota: str):
        super().__init__(fecha, ubicacion, mascota, encuentra_mascota, estado='Encontrada')
