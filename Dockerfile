# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-alpine3.10

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Update packages
RUN apk update upgrade

# Install pip requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# Install database for logins
RUN apk add sqlite-dev

WORKDIR /www
ADD . /www

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Tell docker that all future commands should run as the appuser user
USER appuser

#CMD start the flask server
CMD ["python3", "./app/app.py"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
