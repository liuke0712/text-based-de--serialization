FROM python:alpine
LABEL maintainer="Valroad <valorad@outlook.com>"

ADD . /www/tbds/
WORKDIR /www/tbds

RUN echo " --- Installing Dependencies --- " \
 && apk update \
 && apk add uwsgi uwsgi-python3 su-exec \
 && rm -rf /var/cache/apk/*

RUN echo " --- Collecting Python Wheels --- " \
 && pip install --no-cache-dir -r  requirements.txt

VOLUME ["/www/tbds"]

ENV EXEC_USER=valorad
ENV EXEC_USER_ID=1000
ENV EXEC_PERMISSION=755

RUN echo " --- Fetching + Enabling Entry Script --- " \
#  && wget -O index.sh "https://raw.githubusercontent.com/xmj-alliance/gist/master/docker-entry.sh"
 && chmod +x "/www/tbds/index.sh"

ENTRYPOINT ["/www/tbds/index.sh . ${EXEC_PERMISSION}"]
CMD uwsgi --json "./uwsgi.json" && /bin/sh