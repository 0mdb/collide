FROM pypy:3

WORKDIR /app/

RUN apt-get -y update && \
    apt-get -y install curl \
    build-essential \
    cmake \
    gcc \
    g++ \
    libssl-dev \
    python3.10 \
    python3-distutils \
    wget \
    libpq-dev \
    nano

COPY requirements.txt ./
RUN pypy3 -m pip install -r requirements.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py
COPY start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app /app
ENV PYTHONPATH=/app
EXPOSE 80
# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]