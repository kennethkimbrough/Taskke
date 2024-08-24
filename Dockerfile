# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r taskke/requirements.txt
RUN pip install --no-cache-dir -r crm_chatbot/requirements.txt
# Make port 5000 and 8000 available to the world outside this container
EXPOSE 5000
EXPOSE 8000

# Run task_management and crm_chatbot
CMD ["sh", "-c", "python taskke/app.py & uvicorn crm_chatbot.main:app --host 0.0.0.0 --port 8000"]
