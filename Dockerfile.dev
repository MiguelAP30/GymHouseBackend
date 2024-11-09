FROM python:3.11


RUN mkdir -p /app

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app

EXPOSE 8000

CMD [ "bash", "./init/init.sh" ]
