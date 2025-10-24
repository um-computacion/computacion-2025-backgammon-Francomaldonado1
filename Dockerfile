FROM python:3.11-slim

WORKDIR /app

# Copiar requirements.txt si existe
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copiar todo el código del proyecto
COPY . .

# Por defecto ejecuta la CLI
CMD ["python3", "-m", "Backgammon.Interfaces.CLI"]