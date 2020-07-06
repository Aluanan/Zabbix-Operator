FROM python:3.8-slim

WORKDIR /opt/zabbix

COPY ./zabbix-job/requirements.txt /opt/zabbix/requirements.txt
RUN pip install -r requirements.txt

COPY ./zabbix-job/main.py /opt/zabbix/main.py
RUN chmod +x /opt/zabbix/main.py

ENTRYPOINT ["python", "/opt/zabbix/main.py"]