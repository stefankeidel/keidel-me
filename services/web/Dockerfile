# pull official base image
FROM python:3.8-slim-buster

# create directory for the app user
RUN useradd -ms /bin/bash app
USER root

# extraction tools for textract
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python-dev libxml2-dev libxslt1-dev antiword \
    unrtf poppler-utils tesseract-ocr flac ffmpeg \
    lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

# install python deps
RUN mkdir -p /opt/build/
RUN pip install --upgrade pip
COPY requirements.txt /opt/build/requirements.txt
RUN pip install -r /opt/build/requirements.txt

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# download nltk deps
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
