FROM python:3.8
LABEL authors="Artem Polozov"
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 8001

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]