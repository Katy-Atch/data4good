FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV srvdir /cronjobs

RUN mkdir -p ${srvdir}
WORKDIR ${srvdir}

COPY requirements.txt ${srvdir}
RUN pip3 install -r requirements.txt

COPY . ${srvdir}

RUN apt-get update && apt-get -y install cron

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

ENV PATH "$PATH:${srvdir}"

CMD cron -f