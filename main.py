import requests
from bs4 import BeautifulSoup
import re
import json
import os

# URL base de la documentación de Tailwind
base_url = "https://tailwindcss.com"

# Hacer una solicitud GET a la página principal de la documentación
response = requests.get(base_url + "/docs")
if response.status_code == 200:
    print("Página cargada correctamente")
else:
    print(f"Error al cargar la página: {response.status_code}")
    exit()

# Parsear el contenido HTML de la página principal
soup = BeautifulSoup(response.content, "html.parser")

# Definir el patrón para encontrar los enlaces de la documentación
patron = r"/docs/[\w-]*"

# Definir una lista de palabras clave relacionadas con diseño frontend/UI
categorias_ui = [
    "color", "colors", "background", "size", "sizes", "spacing", "padding", "margin", 
    "typography", "font", "responsive", "display", "flex", "grid", "position", "shadow", 
    "border", "width", "height", "align", "justify", "text", "breakpoint", "gap", "z-index", 
    "radius", "aspect-ratio", "visibility", "opacity"
]

# Encontrar todos los elementos <a> en la página que contengan los enlaces
enlaces = soup.find_all("a", href=re.compile(patron))

# Crear una variable para almacenar todo el contenido de la documentación
contenido_total = ""

# Recorrer todos los enlaces y extraer el contenido de cada página
for enlace in enlaces:
    titulo = enlace.get_text(strip=True)  # Extraer el texto del enlace (el título)
    href = enlace.get("href")  # Obtener el enlace (href)
    
    # Solo proceder si el enlace no está vacío y empieza con /docs/
    if titulo and href and href.startswith("/docs/"):
        # Filtrar solo aquellos títulos que están relacionados con diseño frontend/UI
        if any(categoria in titulo.lower() for categoria in categorias_ui):
            url_completa = base_url + href  # Construir la URL completa de la página
            print(f"Accediendo a: {url_completa}")

            # Hacer una solicitud GET a la página de cada sección de la documentación
            sub_response = requests.get(url_completa)
            if sub_response.status_code == 200:
                # Parsear el contenido HTML de la página
                sub_soup = BeautifulSoup(sub_response.content, "html.parser")
                
                # Extraer el contenido de la página
                contenido = sub_soup.get_text(separator="\n", strip=True)  # Extraer todo el texto de la página
                
                # Concatenar el contenido al total
                contenido_total += contenido + "\n\n"  # Añadir un doble salto de línea entre secciones
            else:
                print(f"Error al acceder a {url_completa}: {sub_response.status_code}")

# Crear el diccionario con la clave "contenido" que contiene todo el contenido extraído
documentacion_json = {"contenido": contenido_total}

# Definir la ruta donde se guardará el archivo JSON dentro del proyecto
ruta_json = os.path.join(os.getcwd(), "documentacion_tailwind.json")

# Guardar los datos en un archivo JSON
with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(documentacion_json, f, ensure_ascii=False, indent=4)

print(f"Documentación guardada en {ruta_json}")
