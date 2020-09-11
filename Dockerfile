# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

WORKDIR /usr/src/backend

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Tells dotenv to load the production environment 
ENV env PROD

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /usr/src/backend
USER appuser

EXPOSE 8000

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
