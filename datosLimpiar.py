
import pandas as pd
import numpy as np

ruta = "P_agresora_Tlaxcala_20251020_191536.xlsx"
df = pd.read_excel(ruta)

print("Archivo cargado ")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
print("="*60)

# quitar espacios
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace(r'[^a-z0-9_]', '', regex=True)
)

# vacíos bai
df.dropna(how='all', inplace=True)

# duplicados bai
df.drop_duplicates(inplace=True)

# quitar espacios
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# aqui es donde le cambiamos lo que estpe vació
valores_por_defecto = {
    'agresores_localidad': 'desconocido',
    'agresores_municipio': 'desconocido',
    'agresores_vinculo': 'desconocido',
    'agresores_entidad': 'desconocido',
    'agresores_escolaridad': 'desconocido',
    'agresores_ocupacion': 'desconocido',
    'agresores_ingreso': 'desconocido',
    'agresores_orientacion_sexual': 'no especificado',
    'agresores_identidad_genero': 'no especificado',
    'agresores_sexo': 'no especificado',
    'victima_sexo': 'no especificado',
    'tipo_de_violencia': 'no especificado',
    'victima_orientacion_sexual': 'no especificado',
    'victima_identidad_genero': 'no especificado',
    'agresores_orientacion_sexual': 'no especificado',
    'tipo_agresor_sexual': 'no especificado',       # temporal
    'acoso_hostigamiento': 'no especificado',       # igual tenmporal
    'agresores_edad': np.nan,
    'victima_edad': np.nan
}
for col, val in valores_por_defecto.items():
    if col in df.columns:
        df[col] = df[col].fillna(val)

# convertir fechas
for col in df.columns:
    if 'fecha' in col:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# checar lo de las fechas por si no existen
for col in df.select_dtypes(include=['datetime']).columns:
    df = df[df[col].notnull()]

# limpiar texto
cols_texto = df.select_dtypes(include='object').columns
for col in cols_texto:
    df[col] = df[col].str.lower().str.strip()

# estandaruzar ctaergorias
if 'sexo' in df.columns:
    mapa_sexo = {
        'f': 'femenino',
        'fem': 'femenino',
        'femenina': 'femenino',
        'm': 'masculino',
        'masc': 'masculino',
        'h': 'masculino'
    }
    df['sexo'] = df['sexo'].replace(mapa_sexo)

if 'tipo_de_violencia' in df.columns:
    df['tipo_de_violencia'] = df['tipo_de_violencia'].replace({
        'fisica': 'física',
        'fisica ': 'física',
        'psicologica': 'psicológica',
        'economica': 'económica'
    })


# CONVERTIR EDADES A NUMÉRICO Y LIMPIAR ERRORES
if 'victima_edad' in df.columns:
    df['victima_edad'] = pd.to_numeric(df['victima_edad'], errors='coerce')
    df.loc[(df['victima_edad'] <= 0) | (df['victima_edad'] >= 120), 'victima_edad'] = np.nan

if 'agresores_edad' in df.columns:
    df['agresores_edad'] = pd.to_numeric(df['agresores_edad'], errors='coerce')
    df.loc[(df['agresores_edad'] <= 0) | (df['agresores_edad'] >= 120), 'agresores_edad'] = np.nan


print("Antes de imputar:")
print(f"Víctimas con edad nula: {df['victima_edad'].isnull().sum()}")
print(f"Agresores con edad nula: {df['agresores_edad'].isnull().sum()}")

# imputar edades con mediana
if 'victima_edad' in df.columns:
    mediana_victima = df['victima_edad'].median()
    df['victima_edad'].fillna(mediana_victima, inplace=True)
    print(f"Mediana edad víctimas: {mediana_victima}")

if 'agresores_edad' in df.columns:
    mediana_agresor = df['agresores_edad'].median()
    df['agresores_edad'].fillna(mediana_agresor, inplace=True)
    print(f"Mediana edad agresores: {mediana_agresor}")

print("\nDespués de imputar:")
print(f"Víctimas con edad nula: {df['victima_edad'].isnull().sum()}")
print(f"Agresores con edad nula: {df['agresores_edad'].isnull().sum()}")

# errores 
if 'edad' in df.columns:
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
    df = df[(df['edad'] > 0) & (df['edad'] < 120)]

# para pruegbas
print(" nulos:")
print(df.isnull().sum())
print("="*60)

print("datoslimpios:")
print(df.head(10))
print("="*60)

# no formato de fecha
for col in df.columns:
    if 'fecha' in col:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')

# guardar limpio
salida = "P_agresora_Tlaxcala_limpio.xlsx"
df.to_excel(salida, index=False)
print(f"limpio: {salida}")
