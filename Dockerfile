# This file is a template, and might need editing before it works on your project.
FROM python:3.7
RUN python --version



RUN apt-get update && apt-get g++ -y && \
    apt-get install -y r-recommended && \
    apt-get install -y python3-dev && \
    pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt


