# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM python:3.4-slim

WORKDIR /data
VOLUME /data
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-setuptools\
    software-properties-common \
    zip \
    python3-pip\
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.5' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

EXPOSE 5001

# The rest of this file just runs an example script.

# If you wanted to use this Dockerfile to run your own app instead, maybe you would do this:
# COPY . /root/your_app_or_whatever
# RUN cd /root/your_app_or_whatever && \
#     pip3 install -r requirements.txt
# RUN whatever_command_you_run_to_start_your_app

#COPY . /root/face_recognition
#RUN cd /root/face_recognition && \
#    pip3 install -r requirements.txt && \
#    python3 setup.py install

#CMD cd /root/face_recognition/examples && \
#    python3 recognize_faces_in_pictures.py

COPY . /root/face_recognition
RUN cd /root/face_recognition && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

CMD cd /root/face_recognition/examples && \
    python3 testweb.py
