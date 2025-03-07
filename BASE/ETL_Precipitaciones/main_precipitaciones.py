import pandas as pd

# --- Extracción ---
input_path = "PRECIPITACIONES.csv"

# 1) Lee el archivo asumiendo que está en UTF-8
df = pd.read_csv(input_path, encoding="utf-8", delimiter=";")

# --- Transformación ---
df.columns = [
    "Año", "Mes", "Fecha", "Dengue", "ENOS_C", "ENOS", "AñoMes", "No_Mes",
    "Temp_Max", "Temp_Min", "Temp_Prom", "Casos_Leptospirosis",
    "Lluvia_Acumulada", "Temporada", "Casos_ESI_IRAG", "FRM",
    "Familias_Afectadas", "Inundaciones", "Encharcamiento",
    "Damnificados_Inundaciones", "Damnificados_Encharcamientos", "Clasificacion_ONI"
]

df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce')

cols_to_numeric = [
    "Dengue", "No_Mes", "Temp_Max", "Temp_Min", "Temp_Prom",
    "Casos_Leptospirosis", "Lluvia_Acumulada", "Casos_ESI_IRAG",
    "FRM", "Familias_Afectadas", "Inundaciones", "Encharcamiento",
    "Damnificados_Inundaciones", "Damnificados_Encharcamientos"
]

for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Carga ---
output_path = "PRECIPITACIONES_ETL.csv"

# 2) Guarda con BOM en UTF-8 (utf-8-sig) y separador ;
df.to_csv(output_path, sep=";", index=False, encoding="utf-8-sig")

print("ETL finalizado. Archivo guardado en:", output_path)
