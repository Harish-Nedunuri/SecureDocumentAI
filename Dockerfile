# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Create and set the working directory
WORKDIR /app

# Copy the all file into the working directory
COPY . /app/

# Install the dependencies
RUN apt-get update \
    && apt-get install -y sqlite3 libsqlite3-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .


# Copy the contents of the local vectorstore folder to the container's vectorstore folder
COPY vectorstore /app/vectorstore

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

