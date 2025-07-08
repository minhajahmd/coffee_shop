FROM python:3.13.5-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY recommendation_objects/ recommendation_objects/
COPY agents/ agents/
COPY agent_controller.py agent_controller.py
COPY main.py main.py

# Testing Dockerfile # To remove later
# COPY test_input.json test_input.json

ENTRYPOINT [ "python", "main.py" ]