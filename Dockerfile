# Use Python 3.12.3-slim as the base image
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the application
EXPOSE 8080

# Default command to run the application
CMD ["python", "src/app.py"]