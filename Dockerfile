# Use an official Python base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies (for Tesseract, OpenCV, Wand, and ImageMagick)
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    imagemagick \
    libmagickwand-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Make sure to download necessary NLTK datasets
RUN python -m nltk.downloader punkt averaged_perceptron_tagger

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
