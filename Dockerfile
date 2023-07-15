FROM python:3.7.4-alpine3.10

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY entrypoint.sh generator.py /
RUN chmod +x /entrypoint.sh /generator.py

ENTRYPOINT ["/entrypoint.sh"]