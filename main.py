#main.py
from funciones import reportar_mascota_perdida, reportar_mascota_encontrada
import webbrowser

# Guardo el último mapa generado para poder mostrarlo con la opción 4 sino no funka
ultimo_mapa = None

# Muestra el menú principal con opciones al usuario
def mostrar_menu():
    print("\nMENÚ DE MASCOTAS")
    print("1. Reportar mascota encontrada")
    print("2. Reportar mascota perdida")
    print("3. Ver listado de mascotas")
    print("4. Ver mapa del último reporte")
    print("5. Salir")

# Función principal del programa
def main():
    global ultimo_mapa # Para poder modificar la variable desde dentro de la función
    while True:
        mostrar_menu()
    
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            reporte = reportar_mascota_encontrada()
            if reporte:
                ultimo_mapa = "mapa_evento_encontrada.html"

        elif opcion == "2":
            reporte = reportar_mascota_perdida()
            if reporte:
                ultimo_mapa = "mapa_evento_perdida.html"

        elif opcion == "3":
            print("Función mostrar listado no la hicimos todavía.")

        elif opcion == "4":
            if ultimo_mapa:
                print("Abriendo el mapa en el navegador...")
                webbrowser.open(ultimo_mapa)
            else:
                print("No hay mapas generados para mostrar.")

        elif opcion == "5":
            print("¡Gracias por usar el sistema de mascotas!")
            break

        else:
            print("Opción no válida. Intentalo de nuevo.")

if __name__ == "__main__":
    main()
