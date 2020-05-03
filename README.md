# Frenchtoastman Zabbix Operator

This repo contains the code for the `frenchtoastman/zabbix-operator`. 

## Operator Scope

This operator is a `clusterScoped` operator.

## Operator defaults

```yaml
instance: zabbix # Namespace created for deployment
state: present
release: 0.0.1
domain: minikube
zabbix_server_replicas: 2
zabbix_web_replicas: 2
zabbix_server_image: zabbix/zabbix-server-pgsql
zabbix_snmp_image: zabbix/zabbix-snmptraps
zabbix_agent_image: zabbix/zabbix-agent
zabbix_web_image: zabbix/zabbix-web-nginx-pgsql
zabbix_tag: alpine-trunk
image_pull_policy: IfNotPresent
database_image: registry.gitlab.com/frenchtoasters/zabbix-operator/zabbix-database-postgres
database_image_tag: latest
database_claim_size: 700M
base64_postgres_password: emFiYml4 # Base64 encoded string for password
```

## Install operator

```bash
$ git clone https://gitlab.com/frenchtoasters/zabbix-operator.git
$ cd zabbix-operator/zabbix-operator
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_zabbixes_crd.yaml
$ kubectl create -f deploy/service_account.yaml
$ kubectl create -f deploy/role.yaml
$ kubectl create -f deploy/role_binding.yaml
$ kubectl create -f deploy/operator.yaml
```

## Test operator locally using minikube

```bash
$ minikube start
$ git clone https://gitlab.com/frenchtoasters/zabbix-operator.git
$ cd zabbix-operator/zabbix-operator
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_zabbixes_crd.yaml
$ kubectl create -f deploy/service_account.yaml
$ kubectl create -f deploy/role.yaml
$ kubectl create -f deploy/role_binding.yaml
$ operator-sdk run --local
```

Once above is running open another `kubectl` window and try installing the minimal cluster

```bash
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_v1alpha1_zabbix_cr.yaml 
```


## Test operator locally using ansible

```bash
$ minikube start
$ git clone https://gitlab.com/frenchtoasters/zabbix-operator.git
$ python -m virtualenv venv
$ source venv/bin/active
$ pip install -r requirements.txt
$ ansible-playbook zabbix-operator/roles/playbook.yml
```

### Known issues

* Labels do not update when changed in cr spec for: namespace, statefulset, deployment