# Biolink-API-FastAPI 🔗 (FastAPI + SQLite + JWT)

Una API moderna y minimalista para gestionar enlaces personalizados, tipo Linktree. Desarrollada con FastAPI, SQLModel, autenticación JWT y lista para desplegar en contenedor Docker (ideal para Cloud Run o Railway).

---

## 🚀 Funcionalidades principales

- Registro y login de usuarios con autenticación JWT 🔐
- Crear, editar y eliminar enlaces personales
- Página pública de enlaces: `/users/{username}/links`
- Contador de clics por enlace
- API documentada con Swagger en `/docs`

---

## 🛠️ Tecnologías utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**
- **SQLModel** (SQLite por defecto)
- **Passlib + Bcrypt** (para passwords)
- **JWT (python-jose)** (tokens)
- **Docker** (contenedorización)
- **Swagger UI** (para pruebas)

---

## 📦 Instalación local

```bash
git clone https://github.com/eliudjosue/biolink-api-fastapi
cd BIOLINK
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📖 Endpoints principales

| Método | Ruta                             | Protegido | Descripción                            |
|--------|----------------------------------|-----------|----------------------------------------|
| POST   | `/register`                      | ❌        | Registro de usuario                    |
| POST   | `/login`                         | ❌        | Login y generación de token            |
| POST   | `/links/`                        | ✅        | Crear un nuevo link                    |
| GET    | `/users/{username}/links`        | ❌        | Obtener links públicos de un usuario   |
| PUT    | `/links/{id}`                    | ✅        | Modificar un link propio               |
| DELETE | `/links/{id}`                    | ✅        | Eliminar un link propio                |
| POST   | `/links/{id}/click`              | ❌        | Contar un clic en el enlace            |

---

## 🔐 Autenticación

El login devuelve un token `access_token` que debe usarse como `Bearer Token` en las rutas protegidas.

---

## 🧪 Pruebas

Puedes usar [Thunder Client](https://www.thunderclient.com/) en VS Code o Swagger UI en:

```
http://localhost:8000/docs
```

---

## 🐳 Docker

```bash
# Construir imagen
docker build -t linkhub-api .

# Correr localmente
docker run -d -p 8000:8000 linkhub-api
```

---


## ✍️ Contribuciones

Pull Requests y sugerencias son bienvenidos. Este proyecto es educativo, pero escalable para producción ligera.

---

## 📄 Licencia

MIT © 2025 - [ELIUD CAMPOS](https://github.com/eliudjosue)
