FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean

RUN apt-get install -y libpq-dev

WORKDIR /code
ADD . /code
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 80
CMD ["gunicorn", "gstore.wsgi:application", "--bind", "0.0.0.0:80"]