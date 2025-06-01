# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy your app code into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Fly.io expects
EXPOSE 8080

# Start the app using Gunicorn on port 8080
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
