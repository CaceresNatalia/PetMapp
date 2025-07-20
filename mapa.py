# Importo librerías necesarias para geolocalización, creación del mapa y abrirlo en navegador
from geopy.geocoders import Nominatim
import folium
import webbrowser

# Función que generar el  mapa a partir de una dirección (string)
def generar_mapa(descripcion_direccion):
 # Convertir dirección a coordenadas
    geolocalizador = Nominatim(user_agent="app-busqueda-mascotas")
    ubicacion = geolocalizador.geocode(descripcion_direccion)
# Si no encuentra coordenadas, se informa al usuario y se termina la función
    if ubicacion is None:
        print(" No se pudo encontrar la ubicación. Revisá la dirección.")
        return
 #  latitud y longitud
    lat = ubicacion.latitude
    lon = ubicacion.longitude

    print(f" Coordenadas encontradas: {lat}, {lon}")

    # Crear el mapa
    mapa = folium.Map(location=[lat, lon], zoom_start=16)

    # Agregar marcador en el puntito donde esta la direccion
    folium.Marker(
        [lat, lon],
        popup=f"Ubicación ingresada: {descripcion_direccion}",
        tooltip="Mascota reportada acá 🐾",
        icon=folium.Icon(color="purple")
    ).add_to(mapa)

    # Guarda el mapa como un archivo de html y lo abre en navegador, en una pestaña
    archivo_mapa = "ubicacion_mascota.html"
    mapa.save(archivo_mapa)
    webbrowser.open(archivo_mapa)

# # Esta parte se ejecuta solo si abrís el archivo directamente para probarlo
if __name__ == "__main__":
    direccion = input("Ingresá la dirección (ej: Av. Corrientes 1234, CABA): ")
    generar_mapa(direccion)

## Agrego validacion
def direccion_valida(direccion):
    geolocalizador = Nominatim(user_agent="app-busqueda-mascotas")
    ubicacion = geolocalizador.geocode(direccion)
    return ubicacion is not None