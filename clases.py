from datetime import datetime
from abc import ABC, abstractmethod

# ----------------- Mascotas ------------------

class Mascota:
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str):
        self.tipo = tipo
        self.nombre = nombre
        self.color = color
        self.edad = edad
        self.tamanio = tamanio
        self.sexo = sexo

    def __str__(self):
        return f"{self.tipo} | {self.nombre} | {self.color} | Edad: {self.edad} | Tamaño: {self.tamanio} | {self.sexo}"


class Perro(Mascota):
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str, raza: str):
        super().__init__(tipo, nombre, color, edad, tamanio, sexo)
        self.raza = raza

    def __str__(self):
        return f"{super().__str__()} | {self.raza}"


class Gato(Mascota):
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, tamanio: str, sexo: str):
        super().__init__(tipo, nombre, color, edad, tamanio, sexo)

    def __str__(self):
        return super().__str__()


class Roedor(Mascota):
    def __init__(self, tipo: str, nombre: str, color: str, edad: int, especie: str, sexo: str):
        super().__init__(tipo, nombre, color, edad, especie, sexo)
        self.especie = especie

    def __str__(self):
        return f"{self.tipo} | {self.nombre} | {self.color} | Edad: {self.edad} | Tipo: {self.especie} | {self.sexo}"


# ----------------- Personas ------------------

class Persona:
    def __init__(self, nombre: str, telefono: str):
        self.nombre = nombre
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} | {self.telefono}"


class Duenio_mascota(Persona):
    def __init__(self, nombre: str, telefono: str):
        super().__init__(nombre, telefono)


class Encuentra_mascota(Persona):
    def __init__(self, nombre: str, telefono: str):
        super().__init__(nombre, telefono)


# ----------------- Reportes ------------------

class Reporte(ABC):
    def __init__(self, fecha: datetime, lugar: str, mascota: Mascota, persona: Persona, estado: str):
        self.fecha = fecha
        self.lugar = lugar
        self.mascota = mascota
        self.persona = persona
        self.estado = estado

    @abstractmethod
    def mostrar_datos(self):
        pass


class Reporte_perdida(Reporte):
    def __init__(self, fecha: datetime, lugar: str, mascota: Mascota, persona: Persona, estado: str):
        super().__init__(fecha, lugar, mascota, persona, estado)

    def __str__(self):
        return f"{self.fecha} | {self.lugar} | {self.mascota} | {self.persona} | Estado: {self.estado}"

    def mostrar_datos(self):
        print(f"""
🐾 Reporte de pérdida:
Fecha: {self.fecha.strftime('%d/%m/%Y')}
Lugar: {self.lugar}
Estado: {self.estado}

📌 Mascota:
{self.mascota}

👤 Dueño:
{self.persona}
""")


class Reporte_encuentro(Reporte):
    def __init__(self, fecha: datetime, lugar: str, mascota: Mascota, persona: Persona, estado: str):
        super().__init__(fecha, lugar, mascota, persona, estado)

    def __str__(self):
        return f"{self.fecha} | {self.lugar} | {self.mascota} | {self.persona} | Estado: {self.estado}"

    def mostrar_datos(self):
        print(f"""
🐾 Reporte de encuentro:
Fecha: {self.fecha.strftime('%d/%m/%Y')}
Lugar: {self.lugar}
Estado: {self.estado}

📌 Mascota:
{self.mascota}

👤 Reportante:
{self.persona}
""")


class Reporte__coincidencia(Reporte):
    def __init__(self, reporte1: Reporte, reporte2: Reporte, persona: Persona, estado: str):
        # El reporte de coincidencia toma como fecha/lugar/mascota los del primer reporte
        super().__init__(reporte1.fecha, reporte1.lugar, reporte1.mascota, persona, estado)
        self.reporte1 = reporte1
        self.reporte2 = reporte2

    def __str__(self):
        return f"{self.fecha} | {self.lugar} | {self.mascota} | {self.persona} | Estado: {self.estado}"

    def mostrar_datos(self):
        print(f"""
📌 Reporte de coincidencia:
Fecha: {self.fecha.strftime('%d/%m/%Y')}
Lugar: {self.lugar}
Estado: {self.estado}

🐶 Mascota:
{self.mascota}

👤 Persona:
{self.persona}
""")
