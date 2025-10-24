import pandas as pd

df = pd.read_excel("P_agresora_Tlaxcala_20251020_191536.xlsx")


print(df.info())
print(df.head())


# borrar vacias
df.dropna(how='all', inplace=True)

# borrar dupes
df.drop_duplicates(inplace=True)

# espacios de más
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# quitar espacios en celdas
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# rellenar valores en los vacios
df.fillna({'municipio': 'Desconocido', 'sexo': 'No especificado'}, inplace=True)

# arreglar fecha
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

# fechas invalidas
df = df[df['fecha'].notnull()]

# minpusculas
cols_texto = ['municipio', 'sexo', 'tipo_de_violencia']
for col in cols_texto:
    if col in df.columns:
        df[col] = df[col].str.lower().str.strip()

# diccionario, por si aplica, cambiar para la columan donde se necesite desúes
mapa_sexo = {'f': 'femenino', 'fem': 'femenino', 'm': 'masculino', 'masc': 'masculino'}
df['sexo'] = df['sexo'].replace(mapa_sexo)

# nulps
print(df.isnull().sum())

# erroress
print(df.describe())

# columnas con errores de edad
if 'edad' in df.columns:
    df = df[(df['edad'] > 0) & (df['edad'] < 120)]


# version limpia
df.to_excel("casos_Tlaxcala_limpio.xlsx", index=False)

