FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /usr/src/app/
RUN mkdir /usr/src/app/static
WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY . /usr/src/app/
