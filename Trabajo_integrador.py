# Trabajo Integrador Mauricio Gomez y Lautaro Gonzalez
import csv
import os
import msvcrt

RUTA_ARCHIVO = "paises.csv"

# --- COLORES Y UTILIDADES PARA LOS MENU ---

try:
    from colorama import init, Fore
    init(autoreset=True)
except:
    class Fore:
        GREEN = ""
        RED = ""
        CYAN = ""
        YELLOW = ""


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausa():
    input("\nPresione ENTER para continuar...")

def exito(msg):
    print(Fore.GREEN + msg)

def error(msg):
    print(Fore.RED + msg)

def info(msg):
    print(Fore.CYAN + msg)

def menu_flechas(opciones, titulo):
    indice = 0
    while True:
        limpiar()
        print("=" * 60)
        print(titulo.center(60))
        print("=" * 60)

        for i, op in enumerate(opciones):
            print(("➜ " if i == indice else "  ") + op)

        tecla = msvcrt.getch()

        if tecla == b'\xe0':
            tecla = msvcrt.getch()
            if tecla == b'H':
                indice = (indice - 1) % len(opciones)
            elif tecla == b'P':
                indice = (indice + 1) % len(opciones)
        elif tecla == b'\r':
            return indice

# --- ARCHIVOS ---

def cargar_csv(ruta):
    paises = []
    try:
        with open(ruta, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    paises.append({
                        "nombre": fila["nombre"],
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"]
                    })
                except:
                    error(f"Error en fila: {fila}")
    except FileNotFoundError:
        info("Archivo no encontrado. Se creará al guardar.")
    return paises

def guardar_csv(ruta, paises):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        campos = ["nombre", "poblacion", "superficie", "continente"]
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(paises)

# --- FUNCIONES PRINCIPALES ---

def mostrar_paises(lista):
    if not lista:
        error("No hay datos para mostrar.")
        return

    print("-" * 90)
    print(f"{'Nombre':20}{'Población':15}{'Superficie':15}{'Continente':20}")
    print("-" * 90)

    for p in lista:
        print(
            f"{p['nombre']:20}"
            f"{p['poblacion']:15,}"
            f"{p['superficie']:15,}"
            f"{p['continente']:20}"
        )

def pedir_entero_positivo(texto):
    while True:
        try:
            valor = int(input(texto))
            if valor <= 0:
                error("Debe ser mayor que 0.")
                continue
            return valor
        except ValueError:
            error("Ingrese un número válido.")



def agregar_pais(paises):
    nombre = input("Nombre: ").strip()

    if not nombre:
        error("Nombre vacío.")
        return

    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            error("Ese país ya existe.")
            return

    poblacion = pedir_entero_positivo("Población: ")
    superficie = pedir_entero_positivo("Superficie: ")

    continente = input("Continente: ").strip()
    if not continente:
        error("Continente vacío.")
        return

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })

    exito("País agregado correctamente.")

def actualizar_pais(paises):
    nombre = input("País a actualizar: ").lower()

    for pais in paises:
        if pais["nombre"].lower() == nombre:
            pais["poblacion"] = pedir_entero_positivo("Nueva población: ")
            pais["superficie"] = pedir_entero_positivo("Nueva superficie: ")
            exito("País actualizado correctamente.")
            return

    error("País no encontrado.")

def buscar_pais(paises):
    texto = input("Buscar: ").lower()
    resultados = [p for p in paises if texto in p["nombre"].lower()]
    mostrar_paises(resultados)

def filtrar_continente(paises):
    cont = input("Continente: ").lower()
    resultados = [p for p in paises if p["continente"].lower() == cont]
    mostrar_paises(resultados)

def filtrar_poblacion(paises):
    minimo = pedir_entero_positivo("Mínimo: ")
    maximo = pedir_entero_positivo("Máximo: ")
    resultados = [p for p in paises if minimo <= p["poblacion"] <= maximo]
    mostrar_paises(resultados)

def filtrar_superficie(paises):
    minimo = pedir_entero_positivo("Mínimo: ")
    maximo = pedir_entero_positivo("Máximo: ")
    resultados = [p for p in paises if minimo <= p["superficie"] <= maximo]
    mostrar_paises(resultados)

def ordenar_paises(paises):
    opciones = ["Nombre", "Población", "Superficie"]
    op = menu_flechas(opciones, "ORDENAR")

    orden = input("Ascendente (A) / Descendente (D): ").lower()
    reverse = orden == "d"

    if op == 0:
        paises.sort(key=lambda x: x["nombre"], reverse=reverse)
    elif op == 1:
        paises.sort(key=lambda x: x["poblacion"], reverse=reverse)
    else:
        paises.sort(key=lambda x: x["superficie"], reverse=reverse)

    mostrar_paises(paises)

def estadisticas(paises):
    if not paises:
        error("No hay datos.")
        return

    mayor = max(paises, key=lambda x: x["poblacion"])
    menor = min(paises, key=lambda x: x["poblacion"])

    prom_pob = sum(p["poblacion"] for p in paises) / len(paises)
    prom_sup = sum(p["superficie"] for p in paises) / len(paises)

    print("\n===== ESTADÍSTICAS =====\n")
    print(f"Mayor población : {mayor['nombre']}")
    print(f"Menor población : {menor['nombre']}")
    print(f"Promedio población : {prom_pob:,.2f}")
    print(f"Promedio superficie : {prom_sup:,.2f}")

    conteo = {}
    for p in paises:
        conteo[p["continente"]] = conteo.get(p["continente"], 0) + 1

    print("\nPaíses por continente")
    for k, v in conteo.items():
        print(f"{k}: {v}")

# --- MENU ---

def menu():
    paises = cargar_csv(RUTA_ARCHIVO)

    opciones = [
        "Agregar país",
        "Actualizar país",
        "Buscar país",
        "Filtrar",
        "Ordenar",
        "Estadísticas",
        "Guardar",
        "Salir"
    ]

    while True:
        op = menu_flechas(opciones, "GESTIÓN DE PAÍSES")

        limpiar()

        if op == 0:
            agregar_pais(paises)

        elif op == 1:
            actualizar_pais(paises)

        elif op == 2:
            buscar_pais(paises)

        elif op == 3:
            sub = menu_flechas(
                ["Continente", "Población", "Superficie"],
                "FILTROS"
            )

            limpiar()

            if sub == 0:
                filtrar_continente(paises)
            elif sub == 1:
                filtrar_poblacion(paises)
            else:
                filtrar_superficie(paises)

        elif op == 4:
            ordenar_paises(paises)

        elif op == 5:
            estadisticas(paises)

        elif op == 6:
            guardar_csv(RUTA_ARCHIVO, paises)
            exito("Datos guardados correctamente.")

        elif op == 7:
            guardar_csv(RUTA_ARCHIVO, paises)
            exito("Saliendo del sistema...")
            break

        pausa()

if __name__ == "__main__":
    menu()
