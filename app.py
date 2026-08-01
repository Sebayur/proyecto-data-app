from flask import Flask, jsonify, render_template
import pandas as pd
from sqlalchemy import create_engine 

engine = create_engine("sqlite:///database/app.db")

app = Flask(__name__)

#Cargar datos
df = pd.read_sql("SELECT * FROM usuarios", engine) # Leé el resultado de la consulta SQL y lo guarda en un DataFrame.
print("APP CORRECTA CARGADA")
@app.route("/")
def home():
       return render_template("index.html")

@app.route('/data')
def data():
    return jsonify(df.to_dict(orient='records'))

@app.route("/usuarios/<int:id>")
def get_usuario(id):
       usuario = df[df["id"] == id]

       if usuario.empty:
              return {"error": "Usuario no encontrado"}, 404
       
       return jsonify(usuario.to_dict(orient="records")[0])

if __name__ == "__main__":
       app.run(debug=True)