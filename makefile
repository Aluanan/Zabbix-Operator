REGISTRY ?= registry.gitlab.com/frenchtoasters/zabbix-operator

latest:
    docker build -t $(REGISTRY)/build:latest -f Dockerfile .
    operator-sdk build $(REGISTRY)/zabbix-operator:latest
    docker build -t $(REGISTRY)/zabbix-database-postgres:latest -f zabbix-database/Dockerfile .

push:
    docker push $(REGISTRY)/build:latest
    docker push $(REGISTRY)/zabbix-operator:latest
    docker push $(REGISTRY)/zabbix-database-postgres:latest