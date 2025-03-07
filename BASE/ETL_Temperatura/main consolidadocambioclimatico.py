import pandas as pd

def extract(file_path):
    """
    Función para extraer datos desde un archivo CSV.
    Prueba varios encodings y omite líneas problemáticas.
    Ajusta el 'sep' al delimitador real de tu archivo.
    """
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                on_bad_lines='skip',
                engine='python',
                sep=';'  # Cambia a ',' si el archivo está separado por comas, o '\t' si es tabulado, etc.
            )
            print(f"Extracción completada con encoding '{encoding}'. Registros leídos: {df.shape[0]}")
            return df
        except UnicodeDecodeError as e:
            print(f"Error al decodificar con encoding '{encoding}': {e}")
        except pd.errors.ParserError as e:
            print(f"Error tokenizando con encoding '{encoding}': {e}")
    
    print("No se pudo decodificar o parsear el archivo con ninguno de los encodings probados.")
    return None

def transform(df):
    """
    Función para transformar los datos:
      - Elimina filas con valores nulos.
      - Convierte la columna 'fecha' a tipo datetime, si existe.
      - Crea una columna 'suma_numeros' con la suma de las columnas numéricas.
    """
    try:
        df = df.dropna()
        print("Se eliminaron filas con valores nulos.")
        
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            print("Columna 'fecha' convertida a datetime.")
        
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            df['suma_numeros'] = df[numeric_cols].sum(axis=1)
            print("Nueva columna 'suma_numeros' creada a partir de la suma de columnas numéricas.")
        else:
            print("No se encontraron columnas numéricas para transformar.")
        
        print("Transformación completada.")
        return df
    except Exception as e:
        print("Error durante la transformación:", e)
        return df

def load_to_excel(df, output_path):
    """
    Función para cargar los datos transformados a un archivo Excel (.xlsx).
    """
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"Carga completada. Archivo Excel guardado en: {output_path}")
    except Exception as e:
        print("Error durante la carga en Excel:", e)

if __name__ == '__main__':
    # Ajusta las rutas a tu entorno real
    input_file = 'Meta_FNCER__Incorporar_en_la_matriz_energ_tica_nueva_capacidad_instalada_a_partir_de_Fuentes_No_Convencionales_de_Energ_a_Renovable_-_FNCER_20250227 (1).csv'
    output_file_excel = 'Meta_FNCER__Incorporar_en_la_matriz_energ_tica_nueva_capacidad_instalada_a_partir_de_Fuentes_No_Convencionales_de_Energ_a_Renovable_-_FNCER_20250227.xlsx'
    
    data = extract(input_file)
    if data is not None:
        print("\nVista previa de los datos extraídos:")
        print(data.head())
        
        data_transformed = transform(data)
        if data_transformed is not None and not data_transformed.empty:
            load_to_excel(data_transformed, output_file_excel)
        else:
            print("El DataFrame transformado está vacío o es None, no se genera archivo de salida.")
