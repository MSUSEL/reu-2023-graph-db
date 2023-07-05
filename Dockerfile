FROM ubuntu:22.04
FROM python:3.10

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

WORKDIR /reu-2023-graph-db
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#COPY ./databaseUpdate . 
COPY ./filePassing .

#CMD ["python3","driver.py"]
CMD python3 -m http.server 8000


