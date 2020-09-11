FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./start.py", "https://www.jobindex.dk/","jobindex.dk"]