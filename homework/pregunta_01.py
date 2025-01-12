import pandas as pd
import re

def pregunta_01():
    # Ruta del archivo
    filepath = 'files/input/clusters_report.txt'

    # Leer el archivo línea por línea
    with open(filepath, "r", encoding='utf-8') as file:
        lines = file.readlines()

    # Variables para almacenar los datos procesados
    data = []
    current_row = {
        "Cluster": None,
        "Cantidad_de_palabras_clave": None, 
        "Porcentaje_de_palabras_clave": None,
        "Principales_palabras_clave": []
    }

    # Expresión regular para detectar líneas que inician con un número (Cluster)
    cluster_start_regex = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s+%')

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Saltar líneas vacías

        # Verificar si la línea inicia con un número (Nuevo Cluster)
        match = cluster_start_regex.match(line)
        if match:
            # Si ya hay datos en current_row, procesarlos y agregarlos a data
            if current_row["Cluster"] is not None:
                # Unir las palabras clave acumuladas, limpiar y formatear
                keywords = ' '.join(current_row["Principales_palabras_clave"])
                keywords = re.sub(r'\s+', ' ', keywords)  # Reducir espacios múltiples
                keywords = re.sub(r',\s*', ', ', keywords)  # Asegurar formato de comas
                keywords = re.sub(r'\s*,\s*', ', ', keywords)  # Eliminar espacios antes de comas
                keywords = keywords.rstrip('.')  # Eliminar punto final si existe
                current_row["Principales_palabras_clave"] = keywords

                data.append(current_row)

            # Extraer datos del nuevo Cluster
            cluster_num = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(',', '.'))

            current_row = {
                "Cluster": cluster_num,
                "Cantidad_de_palabras_clave": cantidad,
                "Porcentaje_de_palabras_clave": porcentaje,
                "Principales_palabras_clave": []
            }

            # Extraer la parte de las palabras clave en la misma línea
            porcentaje_end = match.end()
            keywords_part = line[porcentaje_end:].strip()
            if keywords_part:
                current_row["Principales_palabras_clave"].append(keywords_part)
        else:
            # Continuar acumulando palabras clave en líneas multilínea
            current_row["Principales_palabras_clave"].append(line)

    # Después de procesar todas las líneas, agregar el último registro
    if current_row["Cluster"] is not None:
        keywords = ' '.join(current_row["Principales_palabras_clave"])
        keywords = re.sub(r'\s+', ' ', keywords)
        keywords = re.sub(r',\s*', ', ', keywords)
        keywords = re.sub(r'\s*,\s*', ', ', keywords)
        keywords = keywords.rstrip('.')
        current_row["Principales_palabras_clave"] = keywords
        data.append(current_row)

    # Convertir los datos en un DataFrame
    df = pd.DataFrame(data)

    # Renombrar las columnas: minúsculas y reemplazar espacios por guiones bajos
    df.columns = df.columns.map(lambda x: x.strip().lower().replace(" ", "_"))

    return df
