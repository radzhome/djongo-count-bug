# Using custom image derived from python:3.7-alpine but with all requirements pre-installed
FROM pmdigital/3.7-alpine

# Copy the entire repo to image
COPY . /usr/src/app

# Python pip dependencies
RUN pip3 install -r ./requirements.txt

