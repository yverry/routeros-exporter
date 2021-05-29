#
# Dockerfile
#

FROM python:alpine
MAINTAINER Yann Verry <docker@verry.org>

WORKDIR /app
COPY Pipfile Pipfile.lock main.py /app/

RUN pip install --no-cache-dir pipenv && \
	pipenv install --system --deploy

USER nobody
CMD python /app/main.py