FROM python:3

WORKDIR /app

COPY ./RadarModule .

COPY requirements2.txt .

RUN pip install -r requirements2.txt

CMD ["npm", "install"]

CMD ["docker", "pull rabbitmq:3.9-management"]

CMD ["npm", "run dev"]