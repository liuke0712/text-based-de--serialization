FROM alpine:edge
LABEL maintainer="Valroad <valorad@outlook.com>"

ADD . /www/tbds/
WORKDIR /www/tbds

RUN echo " --- Installing Dependencies --- " \
 && apk update \
 && apk add python3 uwsgi uwsgi-python3 su-exec \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && ln -s /usr/bin/pip3 /usr/bin/pip \
 && python -m pip install --no-cache-dir --upgrade pip \
 && rm -rf /var/cache/apk/*

RUN echo " --- Collecting Python Wheels --- " \
 && pip install --no-cache-dir -r requirements.txt

VOLUME ["/www/tbds/statics"]

ENV EXEC_USER=tbds
ENV EXEC_USER_ID=1000
ENV EXEC_PERMISSION=755

EXPOSE 9000

RUN echo " --- Fetching + Enabling Entry Script --- " \
 && chmod +x "/www/tbds/index.sh"

ENTRYPOINT ["/www/tbds/index.sh"]
CMD uwsgi --json "./uwsgi.json" && /bin/sh