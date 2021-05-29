#
# Dockerfile
#

FROM python:alpine
MAINTAINER Yann Verry <docker@verry.org>

WORKDIR .

RUN pip install --no-cache-dir pipenv && \
	pipenv install --system --deploy

USER nobody
CMD python /routeros-restapi/main.py