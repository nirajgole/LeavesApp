FROM python:3.10-slim

# Install system dependencies for SQL Server (pyodbc)
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Give execution rights to the script
RUN chmod +x /app/prestart.sh

# Use the script to start the container
CMD ["/app/prestart.sh"]