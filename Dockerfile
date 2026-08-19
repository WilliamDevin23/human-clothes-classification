# Use an official Python runtime as the base image
FROM python:3.13.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first (for better caching)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
