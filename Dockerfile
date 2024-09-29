# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install cron and any dependencies (like dotenv)
RUN apt-get update && apt-get install -y cron

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the Python script executable
RUN chmod +x /app/ordwatch.py

# Copy crontab file to the cron.d directory
COPY cronjob /etc/cron.d/ordwatch-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/ordwatch-cron

# Apply the cron job
RUN crontab /etc/cron.d/ordwatch-cron

# Ensure cron is running
CMD ["cron", "-f"]
