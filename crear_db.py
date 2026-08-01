from sqlalchemy import create_engine # conecta python con la base de datos
import pandas as pd # Sirve para leer el csv

engine = create_engine("sqlite:///database/app.db")
df = pd.read_csv("data/data.csv")
df.to_sql( # Guardá este DataFrame dentro de la base de datos.
    "usuarios", # crea una tabla llamada usuarios
    engine, # conexion que hicimos antes
    if_exists="replace", # Cada vez que ejecutes el script: borra la tabla anterior, la vuelve a crear y vuelve a cargar el CSV
    index=False
)
print("Base de datos creada correctamente.")