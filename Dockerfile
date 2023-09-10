# Use the official Python image as a parent image
FROM python:3.9-slim

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=127.0.0.1
ENV FLASK_RUN_PORT=8000  

# Create and set the working directory in the container
WORKDIR /

# Install any necessary dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy your application code into the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 8000

# Start the Flask application and Celery Beat
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=8000 & celery beat"]
