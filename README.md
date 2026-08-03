# Proyecto Data App

Aplicación web desarrollada con Python y Flask para gestionar y visualizar datos de usuarios.

## Tecnologías

- Python
- Flask
- SQLite
- Pandas
- SQLAlchemy
- HTML
- JavaScript

## Funcionalidades actuales

- API REST con Flask
- Base de datos SQLite
- Visualización dinámica de usuarios
- Búsqueda por nombre
- Búsqueda por ciudad
- Creacion de usuarios desde la interfaz
- Eliminar un usuario desde la interfaz
- Editar los datos de un usuario desde la interfaz

## Próximas mejoras

- Dashboard con estadísticas
- Gráficos interactivos
- Importación de CSV
- Exportación a Excel
- Deploy de la aplicación

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Sebayur/proyecto-data-app.git
```

Entrar a la carpeta:

```bash
cd proyecto-data-app
```

Crear un entorno virtual:

### Windows

```bash
python -m venv .venv
```

Activarlo:

```bash
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecutar la aplicación

Si la base de datos todavía no existe:

```bash
python crear_db.py
```

Luego iniciar Flask:

```bash
python app.py
```

Abrir el navegador en:

```
http://127.0.0.1:5000
```

## Autor

**Sebastian Yurtgulu**

Estudiante de Ingeniería Informática (FIUBA)