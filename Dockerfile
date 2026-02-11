# Base Image
FROM python:3.10-slim

# Setup
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Our Package
COPY . .
RUN pip install .

# Default Command: Run the data script
CMD ["python", "-m", "patek_analysis.data"]