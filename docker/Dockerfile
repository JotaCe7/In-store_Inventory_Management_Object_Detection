FROM python:3.8.13 as base

ARG USER_ID
ARG GROUP_ID

# Add a non-root user
RUN addgroup --gid $GROUP_ID app
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID app
USER app

# Install the python packages for this new user
ADD requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /home/app