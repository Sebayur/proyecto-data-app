import io

import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file
from sqlalchemy import text

from database import engine
from validators import validar_usuario

app = Flask(__name__)

def obtener_usuarios():
    consulta = "SELECT * FROM usuarios"
    return pd.read_sql(consulta, engine)
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/data')
def data():
    df = obtener_usuarios()
    return jsonify(df.to_dict(orient='records'))

def obtener_datos_usuario():
    datos = request.json

    nombre = datos["nombre"]
    edad = datos["edad"]
    ciudad = datos["ciudad"]

    error = validar_usuario(nombre, edad, ciudad)

    if error:
        return None, error

    return {
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad
    }, None

@app.route("/agregar", methods=["POST"])
def agregar_usuario():

    datos, error = obtener_datos_usuario()

    if error:
        return {"error": error}, 400

    df = obtener_usuarios()

    nuevo_id = df["id"].max() + 1

    nuevo = pd.DataFrame([{
        "id": nuevo_id,
        "nombre": datos["nombre"],
        "edad": datos["edad"],
        "ciudad": datos["ciudad"]
    }])

    nuevo.to_sql(
        "usuarios",
        engine,
        if_exists="append",
        index=False
    )

    return {"mensaje": "Usuario agregado correctamente"}

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):

    with engine.begin() as conexion:
        resultado = conexion.execute(
            text("DELETE FROM usuarios WHERE id = :id"),
            {"id": id}
        )

    if resultado.rowcount == 0:
        return {"error": "Usuario no encontrado"}, 404

    return {"mensaje": "Usuario eliminado correctamente"}

@app.route("/editar/<int:id>", methods=["PUT"])
def editar_usuario(id):

    datos, error = obtener_datos_usuario()

    if error:
        return {"error": error}, 400

    with engine.begin() as conexion:
        resultado = conexion.execute(
            text("""
                UPDATE usuarios
                SET nombre = :nombre,
                    edad = :edad,
                    ciudad = :ciudad
                WHERE id = :id
            """),
            {
                "id": id,
                "nombre": datos["nombre"],
                "edad": datos["edad"],
                "ciudad": datos["ciudad"]
            }
        )

    if resultado.rowcount == 0:
        return {"error": "Usuario no encontrado"}, 404

    return {"mensaje": "Usuario actualizado correctamente"}

@app.route("/usuarios/<int:id>")
def get_usuario(id):
    df = obtener_usuarios()
    usuario = df[df["id"] == id]

    if usuario.empty:
        return {"error": "Usuario no encontrado"}, 404
       
    return jsonify(usuario.to_dict(orient="records")[0])

@app.route("/export/csv")
def exportar_csv():

    df = obtener_usuarios() 

    buffer = io.StringIO()

    df.to_csv(buffer, index=False)

    buffer.seek(0)

    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="usuarios.csv"
    )

@app.route("/export/xlsx")
def exportar_xlsx():

    df = obtener_usuarios()

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Usuarios"
        )

    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="usuarios.xlsx"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)