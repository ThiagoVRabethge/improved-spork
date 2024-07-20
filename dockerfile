# Use the official Python image as the base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the FastAPI app files into the container
COPY . /app

# Install dependencies
RUN py -m pip install -r requirements.txt

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
