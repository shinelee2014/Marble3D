FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Expose server port
EXPOSE 8000

# Run Python server
CMD ["python", "server.py"]
