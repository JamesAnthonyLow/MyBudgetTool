FROM python:3.11
RUN pip3 install pip-tools pytest mypy black isort

WORKDIR /workspace
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

ENV PYTHONPATH /workspace