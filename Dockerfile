FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set default command (can be overridden when running the container)
# E.g. docker run <image_name> python segmentation.py
CMD ["python", "process.py"]
