FROM python:3.9-slim
WORKDIR /app
COPY ./ /app
RUN pip3 install --default-timeout=1000 --upgrade pip
RUN pip3 install -r requirements.txt --default-timeout=1000 --no-cache-dir