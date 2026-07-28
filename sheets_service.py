import csv
import io
import re
import unicodedata

import requests


# Pega aquí el ID de tu Google Sheets.
SPREADSHEET_ID = "1HktqwQWK5cewOAIENOAMAixQBiLT_IX3Z8QRX3myiNg"

# Nombre exacto de la pestaña.
SHEET_NAME = "Planos"


def normalizar_texto(texto):
    """
    Convierte:
        Montaño -> MONTANO
        instalación eléctrica -> INSTALACION ELECTRICA
    """
    if texto is None:
        return ""

    texto = str(texto).strip().upper()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    texto = re.sub(r"\s+", " ", texto)

    return texto


def obtener_url_csv():
    """
    Genera la URL para leer la pestaña de Google Sheets como CSV.
    """
    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={SHEET_NAME}"
    )


def obtener_planos():
    """
    Lee todas las filas de la pestaña Planos.

    Devuelve una lista de diccionarios:
    [
        {
            "ProyectoCodigo": "MONTANO",
            "TipoPlanoCodigo": "IE",
            "TipoPlano": "Instalación eléctrica",
            ...
        }
    ]
    """
    url = obtener_url_csv()

    response = requests.get(url, timeout=30)

    print("SHEETS STATUS:", response.status_code)
    print("SHEETS CONTENT-TYPE:", response.headers.get("Content-Type"))

    if response.status_code != 200:
        print("SHEETS RESPONSE:", response.text[:500])

        raise RuntimeError(
            f"Google Sheets respondió con HTTP "
            f"{response.status_code}"
        )

    contenido = response.text

    if "<html" in contenido.lower():
        raise RuntimeError(
            "Google devolvió una página HTML en vez del CSV. "
            "Revisa que la hoja tenga acceso mediante enlace."
        )

    lector = csv.DictReader(io.StringIO(contenido))

    filas = []

    for fila in lector:
        fila_limpia = {}

        for columna, valor in fila.items():
            columna_limpia = (
                columna.strip()
                if columna is not None
                else ""
            )

            valor_limpio = (
                valor.strip()
                if isinstance(valor, str)
                else valor
            )

            fila_limpia[columna_limpia] = valor_limpio

        filas.append(fila_limpia)

    return filas


def buscar_planos_por_proyecto(proyecto):
    """
    Busca todos los planos de un proyecto.

    Ejemplos:
        buscar_planos_por_proyecto("Montaño")
        buscar_planos_por_proyecto("MONTANO")
    """
    proyecto_buscado = normalizar_texto(proyecto)
    planos = obtener_planos()

    resultados = []

    for plano in planos:
        proyecto_codigo = normalizar_texto(
            plano.get("ProyectoCodigo")
        )

        carpeta = normalizar_texto(
            plano.get("Carpeta")
        )

        cliente_codigo = normalizar_texto(
            plano.get("ClienteCodigo")
        )

        if proyecto_buscado in {
            proyecto_codigo,
            carpeta,
            cliente_codigo,
        }:
            resultados.append(plano)

    return resultados


def buscar_plano(proyecto, tipo_plano):
    """
    Busca un plano por proyecto y tipo.

    Ejemplos:
        buscar_plano("Montaño", "IE")
        buscar_plano("MONTANO", "Instalación eléctrica")
        buscar_plano("ZIGA", "A")
    """
    proyecto_buscado = normalizar_texto(proyecto)
    tipo_buscado = normalizar_texto(tipo_plano)

    planos = obtener_planos()

    for plano in planos:
        proyecto_codigo = normalizar_texto(
            plano.get("ProyectoCodigo")
        )

        carpeta = normalizar_texto(
            plano.get("Carpeta")
        )

        cliente_codigo = normalizar_texto(
            plano.get("ClienteCodigo")
        )

        tipo_codigo = normalizar_texto(
            plano.get("TipoPlanoCodigo")
        )

        tipo_nombre = normalizar_texto(
            plano.get("TipoPlano")
        )

        proyecto_coincide = proyecto_buscado in {
            proyecto_codigo,
            carpeta,
            cliente_codigo,
        }

        tipo_coincide = tipo_buscado in {
            tipo_codigo,
            tipo_nombre,
        }

        if proyecto_coincide and tipo_coincide:
            return plano

    return None


if __name__ == "__main__":
    print("=== PRUEBA DE GOOGLE SHEETS ===")

    try:
        planos = obtener_planos()

        print(f"Filas encontradas: {len(planos)}")

        if planos:
            print("Columnas detectadas:")
            print(list(planos[0].keys()))

            print("\nPrimera fila:")
            print(planos[0])

        print("\nBuscando MONTANO + IE:")

        resultado = buscar_plano(
            proyecto="MONTANO",
            tipo_plano="IE",
        )

        print(resultado)

    except Exception as error:
        print("ERROR:", error)