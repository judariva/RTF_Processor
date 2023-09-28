# ------------------------------------------------------------------------------
# Nombre del archivo: rtf_processor.py
# Autor: Juan David Rivera Valero
# Sitio Web: https://juandavidrivera.com
# Fecha de creación: 28/09/2023]
# Copyright © 2023 Juan David Rivera Valero. Todos los derechos reservados.
#
# Descripción:
# Este script procesa archivos RTF, extrae información relevante de ellos y 
# la guarda en un archivo Excel. Busca códigos de programas y sus descripciones 
# dentro de los archivos RTF y los compila en un archivo Excel.
# ------------------------------------------------------------------------------

import os
import re
import pandas as pd

# Compilación de la expresión regular para identificar y extraer códigos de programas y descripciones
PROGRAM_REGEX = re.compile(r'\s+([A-Z0-9]+)\s+(.+)')

def is_rtf_file(file_path):
    """Determina si un archivo es RTF basándose en su contenido."""
    with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
        header = f.read(5)
    return header == '{\\rtf'

def rtf_to_text(rtf_path):
    """Convierte un archivo RTF a texto plano."""
    with open(rtf_path, 'r', encoding='latin-1') as f:
        return f.read()

def extract_data_from_text(text):
    """Extrae códigos de programas y sus descripciones del texto."""
    lines = text.split('\\line')
    return [
        [program.strip(), description.strip()]
        for line in lines
        if not ("LISTADO" in line or "\\u9474|" in line)
        if (match := PROGRAM_REGEX.search(line))
        for program, description in [match.groups()]
    ]

def main():
    """Función principal que coordina el proceso de extracción y guardado de datos."""
    rtf_dir = os.path.dirname(os.path.abspath(__file__))
    output_excel_path = os.path.join(rtf_dir, 'output.xlsx')

    # Obtener todos los archivos RTF del directorio actual
    rtf_paths = [os.path.join(rtf_dir, f) for f in os.listdir(rtf_dir) if is_rtf_file(os.path.join(rtf_dir, f))]
    if not rtf_paths:
        print("No se encontraron archivos RTF en el directorio especificado.")
        return

    # Procesar los archivos RTF y extraer los datos
    df_list = [
        pd.DataFrame(extract_data_from_text(rtf_to_text(rtf_path)), columns=['Código de Programa', 'Descripción del Programa'])
        for rtf_path in rtf_paths
        if extract_data_from_text(rtf_to_text(rtf_path))
    ]

    if not df_list:
        print("No se encontraron datos válidos en los archivos RTF.")
        return

    # Guardar la información extraída en un archivo Excel
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_excel(output_excel_path, index=False)

if __name__ == '__main__':
    main()
