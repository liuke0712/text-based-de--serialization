FROM python:alpine
LABEL maintainer="Valroad <valorad@outlook.com>"

ADD . /www/tbds/
WORKDIR /www/tbds

RUN echo " --- Installing Dependencies --- " \
 && apk update \
 && apk add su-exec \
 && rm -rf /var/cache/apk/*

RUN echo " --- Collecting Python Wheels --- " \
 && pip install --no-cache-dir -r requirements.txt

VOLUME ["/www/tbds/statics"]

ENV EXEC_USER=tbds
ENV EXEC_USER_ID=1000
ENV EXEC_PERMISSION=755

EXPOSE 5000

RUN echo " --- Fetching + Enabling Entry Script --- " \
 && chmod +x "/www/tbds/index.sh"

ENTRYPOINT ["/www/tbds/index.sh"]
CMD python main.py && /bin/sh