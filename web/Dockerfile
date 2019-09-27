FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV srvdir /code

RUN mkdir -p ${srvdir}
WORKDIR ${srvdir}

COPY requirements.txt ${srvdir}
RUN pip3 install -r requirements.txt

COPY . ${srvdir}

RUN chmod +x entrypoint.sh

ENV PATH "$PATH:${srvdir}"

ENTRYPOINT ["entrypoint.sh"]