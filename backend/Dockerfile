# Get a Python container (like a plain box)
FROM python:3.11-slim

# Make a workspace inside the box
WORKDIR /app

# Copy our math tools inside
COPY ./app ./app

# Copy the grocery list
COPY requirements.txt .

# Go shopping! Install what's on the list
RUN pip install --no-cache-dir -r requirements.txt

# When box opens, start the brain
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]