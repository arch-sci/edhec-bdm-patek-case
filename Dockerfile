# Base Image
FROM python:3.10-slim

# Setup
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Our Package
COPY . .
RUN pip install .

# Default Command: This tells Docker: "As soon as you wake up, run the main analysis pipeline."
CMD ["python", "-m", "patek_analysis.data"]
# We tried to tell it to run data.py AND model.py .. to show that we can. it worked
# CMD ["sh", "-c", "python -m patek_analysis.data && python -m patek_analysis.model"] 