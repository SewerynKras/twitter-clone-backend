# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

WORKDIR /usr/src/backend

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Tells dotenv to load the production environment 
ENV env PROD

# Update the package list and install netcat (it's used inside the entrypoint script)
RUN apt-get update && apt-get -y install netcat

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /usr/src/backend
USER appuser

EXPOSE 8000

# Wait for postgres to finish initialing and run django migrations
ENTRYPOINT [ "/usr/src/backend/entrypoint.sh" ]
