# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos necesarios al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto por el que Cloud Run espera recibir tráfico
EXPOSE 8080

# Comando para ejecutar la aplicación (en el puerto correcto)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
