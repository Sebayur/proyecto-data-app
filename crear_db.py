import pandas as pd
from database import engine


df = pd.read_csv("data/data.csv")

df.to_sql(
    "usuarios",
    engine,
    if_exists="replace",
    index=False
)

print("Base de datos creada correctamente.")