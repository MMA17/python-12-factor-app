FROM python:3.7-slim

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y libpq-dev gcc net-tools curl
RUN pip3 install psycopg2~=2.6
RUN apt-get autoremove -y gcc
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN chmod +x run.sh

EXPOSE 5000
EXPOSE 8000

CMD ./run.sh