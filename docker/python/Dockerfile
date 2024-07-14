FROM python:3.11.9
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    sudo \
    wget \
    vim  
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip
RUN mv chromedriver-linux64/chromedriver /usr/bin/
RUN apt install -y libnss3
RUN apt install -y cron
RUN apt install -y nano
WORKDIR /work
CMD ["/bin/bash"] 

