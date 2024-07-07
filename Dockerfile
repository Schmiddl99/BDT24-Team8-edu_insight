# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the service account JSON file into the container
COPY cloud/bdt-2024-accesskey.json /app/cloud/bdt-2024-accesskey.json

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the environment variable to point to the service account JSON file
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/cloud/bdt-2024-accesskey.json"

# Set the command to run the Streamlit app
CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]