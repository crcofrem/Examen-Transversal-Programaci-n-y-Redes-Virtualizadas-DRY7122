import requests

# ============================
# API KEY DE GRAPHHOPPER
# ============================
API_KEY = "958b82a3-5906-4547-88fe-10fe778e7ed3"

# Medios de transporte disponibles
transportes = {
    "1": ("Automóvil", "car"),
    "2": ("Bicicleta", "bike"),
    "3": ("Caminando", "foot")
}


def obtener_coordenadas(ciudad):
    url = "https://nominatim.openstreetmap.org/search"

    parametros = {
        "q": ciudad,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "PythonGraphHopper"
    }

    respuesta = requests.get(url, params=parametros, headers=headers)

    datos = respuesta.json()

    if len(datos) == 0:
        return None

    lat = datos[0]["lat"]
    lon = datos[0]["lon"]

    return lat, lon


def calcular_ruta(origen, destino, vehiculo):

    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)

    if coord_origen is None or coord_destino is None:
        print("\nNo se encontró alguna ciudad.\n")
        return

    url = "https://graphhopper.com/api/1/route"

    parametros = {
        "point": [
            f"{coord_origen[0]},{coord_origen[1]}",
            f"{coord_destino[0]},{coord_destino[1]}"
        ],
        "profile": vehiculo,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)

    datos = respuesta.json()

    if "paths" not in datos:
        print("\nError al calcular la ruta.")
        print(datos)
        return

    ruta = datos["paths"][0]

    km = ruta["distance"] / 1000
    millas = km * 0.621371
    tiempo = ruta["time"] / 1000

    horas = int(tiempo // 3600)
    minutos = int((tiempo % 3600) // 60)

    print("\n==============================")
    print("INFORMACIÓN DEL VIAJE")
    print("==============================")
    print(f"Origen: {origen}")
    print(f"Destino: {destino}")
    print(f"Distancia: {km:.2f} km")
    print(f"Distancia: {millas:.2f} millas")
    print(f"Duración: {horas} horas {minutos} minutos")

    print("\nNarrativa del viaje:\n")

    for paso in ruta["instructions"]:
        print("-", paso["text"])

    print()


while True:

    print("====================================")
    print(" SISTEMA DE VIAJES CHILE - PERÚ")
    print("====================================")
    print("1. Consultar viaje")
    print("S. Salir")

    opcion = input("\nSeleccione una opción: ").lower()

    if opcion == "s":
        print("\nHasta luego.")
        break

    if opcion != "1":
        print("\nOpción inválida.\n")
        continue

    origen = input("\nCiudad de origen (Chile): ")
    destino = input("Ciudad de destino (Perú): ")

    print("\nSeleccione transporte")
    print("1. Automóvil")
    print("2. Bicicleta")
    print("3. Caminando")

    medio = input("\nOpción: ")

    if medio not in transportes:
        print("\nOpción incorrecta.\n")
        continue

    nombre, perfil = transportes[medio]

    print(f"\nCalculando ruta en {nombre}...\n")

    calcular_ruta(origen, destino, perfil)