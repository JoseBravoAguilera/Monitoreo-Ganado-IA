# Usamos una versión ligera de Python
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiamos los requisitos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la IA
COPY ia_ganado.py .

# Comando para iniciar (OJO: Asegúrate que el nombre del archivo coincida)
CMD ["python", "ia_ganado.py"]