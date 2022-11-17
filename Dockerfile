FROM python:3.10

WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD api2uml /app

CMD ["python", "api2uml.py"]