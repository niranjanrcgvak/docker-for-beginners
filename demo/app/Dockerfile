# 1. Start from a small official Python base image
FROM python:3.12-slim

# 2. Work inside /app in the container
WORKDIR /app

# 3. Copy requirements FIRST so Docker can cache the install layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the source code
COPY . .

# 5. Run as a non-root user (good security habit)
RUN useradd --create-home appuser
USER appuser

# 6. Document the port and define the start command
EXPOSE 5000
CMD ["python", "app.py"]
