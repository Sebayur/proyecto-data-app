import pandas as pd
import pytest
from sqlalchemy import create_engine, text

import app as app_module

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Crear una base de datos SQLite temporal para los tests
    db_path = tmp_path / "test.db"
    test_engine = create_engine(f"sqlite:///{db_path}")

    # Crear la tabla usuarios
    with test_engine.begin() as conexion:
        conexion.execute(text("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                ciudad TEXT NOT NULL
            )
        """))

    # Insertar un usuario inicial
    usuarios = pd.DataFrame([
        {
            "id": 1,
            "nombre": "Pedro",
            "edad": 25,
            "ciudad": "Buenos Aires"
        }
    ])

    usuarios.to_sql(
        "usuarios",
        test_engine,
        if_exists="append",
        index=False
    )

    # Reemplazar el engine real por el de prueba
    monkeypatch.setattr(app_module, "engine", test_engine)

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as client:
        yield client

    test_engine.dispose()

def test_obtener_usuario(client):
    response = client.get("/usuarios/1")

    assert response.status_code == 200

    usuario = response.get_json()

    assert usuario["id"] == 1
    assert usuario["nombre"] == "Pedro"
    assert usuario["edad"] == 25
    assert usuario["ciudad"] == "Buenos Aires"

def test_agregar_usuario(client):
    response = client.post(
        "/agregar",
        json={
            "nombre": "Juan",
            "edad": 30,
            "ciudad": "Rosario"
        }
    )

    assert response.status_code == 200

    datos = response.get_json()

    assert datos["mensaje"] == "Usuario agregado correctamente"

    response = client.get("/data")

    usuarios = response.get_json()

    assert len(usuarios) == 2
    assert any(usuario["nombre"] == "Juan" for usuario in usuarios)

def test_agregar_usuario_con_datos_invalidos(client):
    response = client.post(
        "/agregar",
        json={
            "nombre": "A",
            "edad": 30,
            "ciudad": "Rosario"
        }
    )

    assert response.status_code == 400

    datos = response.get_json()

    assert datos["error"] == \
        "El nombre debe tener al menos 2 caracteres."

def test_editar_usuario(client):
    response = client.put(
        "/editar/1",
        json={
            "nombre": "Pedro Actualizado",
            "edad": 26,
            "ciudad": "La Plata"
        }
    )

    assert response.status_code == 200

    datos = response.get_json()

    assert datos["mensaje"] == "Usuario actualizado correctamente"

    response = client.get("/usuarios/1")

    usuario = response.get_json()

    assert usuario["nombre"] == "Pedro Actualizado"
    assert usuario["edad"] == 26
    assert usuario["ciudad"] == "La Plata"

def test_editar_usuario_con_datos_invalidos(client):
    response = client.put(
        "/editar/1",
        json={
            "nombre": "Pedro",
            "edad": 150,
            "ciudad": "La Plata"
        }
    )

    assert response.status_code == 400

    datos = response.get_json()

    assert datos["error"] == \
        "La edad debe estar entre 0 y 120."

def test_eliminar_usuario(client):
    response = client.delete("/eliminar/1")

    assert response.status_code == 200

    datos = response.get_json()

    assert datos["mensaje"] == "Usuario eliminado correctamente"

    response = client.get("/usuarios/1")

    assert response.status_code == 404

def test_usuario_inexistente(client):
    response = client.get("/usuarios/999")

    assert response.status_code == 404

    datos = response.get_json()

    assert datos["error"] == "Usuario no encontrado"

def test_editar_usuario_inexistente(client):
    response = client.put(
        "/editar/999",
        json={
            "nombre": "Juan",
            "edad": 30,
            "ciudad": "Rosario"
        }
    )

    assert response.status_code == 404

def test_eliminar_usuario_inexistente(client):
    response = client.delete("/eliminar/999")

    assert response.status_code == 404

def test_exportar_csv(client):
    response = client.get("/export/csv")

    assert response.status_code == 200
    assert response.mimetype == "text/csv"

    contenido = response.data.decode("utf-8")

    assert "id,nombre,edad,ciudad" in contenido
    assert "Pedro" in contenido

def test_exportar_xlsx(client):
    response = client.get("/export/xlsx")

    assert response.status_code == 200

    assert (
        response.mimetype
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    assert len(response.data) > 0

def test_agregar_usuario_sin_json(client):
    response = client.post("/agregar")

    assert response.status_code == 400
    assert response.get_json()["error"] == \
        "Se deben enviar datos en formato JSON."


def test_agregar_usuario_con_json_no_objeto(client):
    response = client.post(
        "/agregar",
        json=["Juan", 30, "Rosario"]
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == \
        "Se deben enviar datos en formato JSON."


def test_agregar_usuario_con_campos_faltantes(client):
    response = client.post(
        "/agregar",
        json={
            "nombre": "Juan",
            "edad": 30
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == \
        "Faltan campos obligatorios."
