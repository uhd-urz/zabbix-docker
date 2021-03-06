FROM docker.io/monitoringartist/zabbix-3.0-xxl:3.0.4
MAINTAINER Thomas Hochstrasser <thomas.hochstrasser@stud.uni-heidelberg.de>

ENV \
	SNMPTRAP_enabled=true \
	ZS_SNMPTrapperFile=/tmp/zabbix_traps.tmp \
	ZS_StartSNMPTrapper=1 \
	ZJ_TIMEOUT=10 \
	XXL_grapher=true

COPY default-99-ssl.conf /data/conf/nginx/conf.d/
COPY scripts/ /usr/local/share/zabbix/

RUN touch $ZS_SNMPTrapperFile && \
	yum install -y net-snmp-devel gcc python-devel python-pip && \
	pip install easysnmp && \
	chmod +x /usr/local/share/zabbix/alertscripts/growlmessage.py && \
	chmod +x /usr/local/share/zabbix/externalscripts/polling_data.py && \
	yum remove -y net-snmp-devel gcc python-devel python-pip
