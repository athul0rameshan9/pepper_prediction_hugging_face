# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .
RUN mkdir uploads

# Expose the port Hugging Face expects
EXPOSE 7860

# Command to run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
