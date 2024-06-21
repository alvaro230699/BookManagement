FROM python:3.8.12-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /site

ARG DJANGO_ENV=production
ADD requirements.txt /site/

RUN \
    apk add --no-cache build-base python3-dev py-pip git && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
COPY ./ /site
RUN chmod +x ./infrastructure/docker-entrypoint.sh

CMD [ "sh", "./infrastructure/docker-entrypoint.sh" ]