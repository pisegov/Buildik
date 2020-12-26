FROM alpine:3.7 

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 sqlite build-base python3-dev libffi-dev libressl-dev musl-dev && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

# COPY buildik_proj/pccomponents /usr/src/app

# COPY buildik_proj/server /usr/src/app

# COPY buildik_proj/setups /usr/src/app

# COPY buildik_proj/static /usr/src/app

# COPY buildik_proj/users /usr/src/app

# COPY buildik_proj/db.sqlite3 /usr/src/app

# COPY buildik_proj/manage.py /usr/src/app

COPY ./buildik_proj /usr/src/app/

COPY requirements.txt /usr/src/app

# RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

# RUN export PORT="8000"

# CMD ["source", "env/bin/activate"]
CMD ["sh", "start-heroku.sh"]


