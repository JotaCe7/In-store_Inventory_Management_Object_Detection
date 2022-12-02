FROM python:3.8.13 as base

ARG USER_ID
ARG GROUP_ID

# Install some packages
# ffmpeg libsm6 libxext6 -> opencv
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3.8-dev \
    python3-pip \
    ffmpeg \  
    libsm6 \
    libxext6 \
    nano \
    wget \
    curl

# Add a non-root user
RUN addgroup --gid $GROUP_ID app
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID app

RUN apt-get install -y curl
USER app

# Install the python packages for this new user
COPY requirements.txt .
RUN pip3 install -r requirements.txt


RUN mkdir -p /home/app/scripts
COPY download-vs-code-server.sh /home/app/scripts
WORKDIR /home/app
USER root
RUN chmod +x /home/app/scripts/download-vs-code-server.sh
RUN chown app /home/app/scripts/download-vs-code-server.sh
USER app
RUN /home/app/scripts/download-vs-code-server.sh
USER root
COPY add_env_path.sh /home/app/scripts
RUN chmod +x /home/app/scripts/add_env_path.sh
USER app

WORKDIR /home/app

# Run script to add code-server to PATH and install aditional extensions
# Call run docker without 'bash' at the end
CMD "." "/home/app/scripts/add_env_path.sh" ;"bash"
