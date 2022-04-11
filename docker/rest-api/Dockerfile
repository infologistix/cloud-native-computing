FROM python:alpine

# changed User Directory
WORKDIR /usr/src/app

# Installing requirements
RUN ["pip", "install", "flask"]

# Copying source code to destination in container
COPY ./src /usr/src/app

# expose port 8080
EXPOSE 8080

# Run the application
CMD ["python3", "default.py"]
