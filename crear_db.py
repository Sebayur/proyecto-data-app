import pandas as pd

from sqlalchemy import text

from database import engine


with engine.begin() as conexion:

    conexion.execute(text("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            ciudad TEXT NOT NULL
        )
    """))

    cantidad = conexion.execute(
        text("SELECT COUNT(*) FROM usuarios")
    ).scalar_one()

    if cantidad == 0:
        df = pd.read_csv("data/data.csv")

        df.to_sql(
            "usuarios",
            conexion,
            if_exists="append",
            index=False
        )

        print("Datos iniciales importados correctamente.")

    else:
        print("La tabla ya contiene usuarios. No se importaron datos.")


print("Base de datos inicializada correctamente.")
