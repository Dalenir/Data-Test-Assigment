FROM python:3.12.0-bookworm as core

ENV PYTHONUNBUFFERED=1

LABEL version = '0.0.1'

WORKDIR /sending_service
COPY . ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

## And at this point I like to make another stage with test dependencies and target this stage in dev_compose