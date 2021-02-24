FROM python:3.7.9-slim-buster
LABEL author="theoohoho"

RUN apt update
RUN apt install -y vim
RUN mkdir /urmart
COPY ./ /urmart/
WORKDIR /urmart
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py loaddata dump.json

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]