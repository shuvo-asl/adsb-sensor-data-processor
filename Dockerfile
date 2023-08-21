# Use and official python runtime as the base image
FROM python:3.8
# Set the authors label
LABEL authors="Shuvo"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]