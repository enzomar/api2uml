FROM python:3.10

LABEL maintainer="Vincenzo MARAFIOTI enzo.mar@gmail.com"

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

ADD api2uml /app
ADD entrypoint.sh /app
ADD gunicorn_config.py /app

#CMD ["python", "api2umlweb.py"]

RUN pip3 install gunicorn

ENTRYPOINT ["sh", "entrypoint.sh"]

