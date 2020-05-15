FROM python:3.8-slim-buster

WORKDIR code

#ENV FLASK_APP app.py
#ENV FLASK_RUN_HOST 0.0.0.0


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY install-packages.sh .
RUN ./install-packages.sh

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY * /code/

# CMD python app.py
#CMD ["python wsgi.py"]
