
from datetime import datetime
from clases import Perro, Gato, Roedor, Duenio_mascota, Encuentra_mascota, Reporte, Reporte_perdida, Reporte_encuentro, Reporte__coincidencia
from diccionarios import *

# ------------------ ENCUENTRO ------------------

def crear_reporte_encuentro(datos: dict):
    try:
        persona = datos["persona"]
        mascota = datos["mascota"]
        evento = datos["evento"]

        encuentra_mascota = Encuentra_mascota(persona["nombre"], persona["telefono"])

        tipo = mascota["tipo"]
        if tipo == "Perro":
            m = Perro(tipo, mascota.get("nombre", ""), mascota["color"], 0, mascota["tamano"], mascota["sexo"], mascota["raza"])
        elif tipo == "Gato":
            m = Gato(tipo, mascota.get("nombre", ""), mascota["color"], 0, mascota["tamano"], mascota["sexo"])
        elif tipo == "Roedor":
            m = Roedor(tipo, mascota.get("nombre", ""), mascota["color"], 0, mascota["subtipo"], mascota["sexo"])
        else:
            return None

        fecha = datetime.strptime(evento["fecha"], "%d/%m/%Y")
        lugar = evento["lugar"]
        estado = "Encontrada"

        return Reporte_encuentro(fecha, lugar, m, encuentra_mascota, estado)

    except Exception as e:
        print("Error creando reporte de encuentro:", e)
        return None


def guardar_reporte_encuentro(datos: dict):
    reporte = crear_reporte_encuentro(datos)
    if reporte:
        lista_reportes_encuentro.append(reporte)
        return True
    return False


def obtener_reportes_encuentro():
    return lista_reportes_encuentro


# ------------------ PÉRDIDA ------------------

def crear_reporte_perdida(datos: dict):
    try:
        persona = datos["persona"]
        mascota = datos["mascota"]
        evento = datos["evento"]

        dueno = Duenio_mascota(persona["nombre"], persona["telefono"])

        tipo = mascota["tipo"]
        if tipo == "Perro":
            m = Perro(tipo, mascota["nombre"], mascota["color"], 0, mascota["tamano"], mascota["sexo"], mascota["raza"])
        elif tipo == "Gato":
            m = Gato(tipo, mascota["nombre"], mascota["color"], 0, mascota["tamano"], mascota["sexo"])
        elif tipo == "Roedor":
            m = Roedor(tipo, mascota["nombre"], mascota["color"], 0, mascota["subtipo"], mascota["sexo"])
        else:
            return None

        fecha = datetime.strptime(evento["fecha"], "%d/%m/%Y")
        lugar = evento["lugar"]
        estado = "Perdida"

        return Reporte_perdida(fecha, lugar, m, dueno, estado)

    except Exception as e:
        print("Error creando reporte de pérdida:", e)
        return None


def guardar_reporte_perdida(datos: dict):
    try:
        reporte = crear_reporte_perdida(datos)
        if reporte:
            lista_reportes_perdida.append(reporte)
            print("Reporte guardado:", reporte)
            print("Cantidad actual:", len(lista_reportes_perdida))  
            return True
        return False
    except Exception as e:
        print("Error creando reporte de pérdida:", e)
        return None


def obtener_reportes_perdida():
    return lista_reportes_perdida


# ------------------ FILTRADO ------------------

def filtrar_reportes(reportes, tipo=None, color=None, zona=None):
    resultados = []
    for r in reportes:
        if tipo and r.mascota.tipo.lower() != tipo.lower():
            continue
        if color and color.lower() not in r.mascota.color.lower():
            continue
        if zona and zona.lower() not in r.lugar.lower():
            continue
        resultados.append(r)
    return resultados
