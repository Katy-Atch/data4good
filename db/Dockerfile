FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV srvdir /db

RUN mkdir -p ${srvdir}
WORKDIR ${srvdir}
COPY . ${srvdir}
RUN chmod +x entrypoint.sh

ENV PATH "$PATH:${srvdir}"

ENTRYPOINT ["entrypoint.sh"]
