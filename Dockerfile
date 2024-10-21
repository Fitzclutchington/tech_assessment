FROM python:3.10-slim

WORKDIR /vehicle-query

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .

# Install any required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "vehicle-query.app:app", "--host", "0.0.0.0", "--port", "8000"]
