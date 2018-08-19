FROM ubuntu:17.10

# Setup

RUN apt-get update
RUN apt-get install -y nodejs npm python3-pip git
RUN apt-get upgrade -y

ADD . /app
WORKDIR /app

# Build frontend

RUN npm install frontend
RUN npm run --prefix frontend build

# Install backend dependencies

RUN pip3 install -r backend/requirements.txt
