FROM python:3.6-slim

RUN mkdir camera
WORKDIR camera
COPY / /camera
RUN mkdir images

RUN apt-get update && apt-get install -y build-essential \
    cmake \
    wget \
    git \
    libgtk2.0-dev \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*



RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "/camera/main.py"]
