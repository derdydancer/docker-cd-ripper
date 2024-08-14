# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask flask-sqlalchemy

# Install cdparanoia and ffmpeg
RUN apt-get update && apt-get install -y \
    cdparanoia \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Make port 5009 available to the world outside this container
EXPOSE 5009

# Run app.py when the container launches
CMD ["python", "app.py"]