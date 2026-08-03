from flask import Flask, jsonify, render_template, request
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///database/app.db")

app = Flask(__name__)

#Cargar datos
def obtener_usuarios():
    return pd.read_sql("SELECT * FROM usuarios", engine) # Leé el resultado de la consulta SQL y lo guarda en un DataFrame.
print("APP CORRECTA CARGADA")
@app.route("/")
def home():
       return render_template("index.html")

@app.route('/data')
def data():
    df = obtener_usuarios()
    return jsonify(df.to_dict(orient='records'))

@app.route("/agregar", methods=["POST"])
def agregar_usuario():

    datos = request.json

    nombre = datos["nombre"]
    edad = datos["edad"]
    ciudad = datos["ciudad"]

    df = obtener_usuarios()

    nuevo_id = df["id"].max() + 1

    nuevo = pd.DataFrame([{
        "id": nuevo_id,
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad
    }])

    nuevo.to_sql(
        "usuarios",
        engine,
        if_exists="append",
        index=False
    )

    return {"mensaje": "Usuario agregado correctamente"}

@app.route("/eliminar/<int:id>", methods=["DELETE"]) #Cuando JavaScript llame: DELETE /eliminar/5 Flask ejecutará el SQL: DELETE FROM usuarios WHERE id = 5; y responderá: "mensaje": "Usuario eliminado correctamente"
def eliminar_usuario(id):

    with engine.begin() as conexion:
        conexion.execute(
            text("DELETE FROM usuarios WHERE id = :id"),
            {"id": id}
        )

    return {"mensaje": "Usuario eliminado correctamente"}

@app.route("/editar/<int:id>", methods=["PUT"])
def editar_usuario(id):

    datos = request.json

    nombre = datos["nombre"]
    edad = datos["edad"]
    ciudad = datos["ciudad"]

    with engine.begin() as conexion:
        conexion.execute(
            text("""
                UPDATE usuarios
                SET nombre = :nombre,
                    edad = :edad,
                    ciudad = :ciudad
                WHERE id = :id
            """),
            {
                "id": id,
                "nombre": nombre,
                "edad": edad,
                "ciudad": ciudad
            }
        )

    return {"mensaje": "Usuario actualizado correctamente"}

@app.route("/usuarios/<int:id>")
def get_usuario(id):
       df = obtener_usuarios()
       usuario = df[df["id"] == id]

       if usuario.empty:
              return {"error": "Usuario no encontrado"}, 404
       
       return jsonify(usuario.to_dict(orient="records")[0])

if __name__ == "__main__":
       app.run(debug=True)