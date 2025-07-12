FROM python:3.11-slim

# Set working directory
WORKDIR /grocery-store

# Copy code and install Python packages as root
COPY src/ /grocery-store

RUN pip install --no-cache-dir -r requirements.txt

# Expose and run
EXPOSE 5000
CMD ["python", "run.py"]
