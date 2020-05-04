# Frenchtoastman Zabbix Operator

This repo contains the code for the `frenchtoastman/zabbix-operator`. 

## Operator Scope

This operator is a `clusterScoped` operator. See more information about operator scope 
[here](https://github.com/operator-framework/operator-sdk/blob/master/website/content/en/docs/operator-scope.md).

***Note*** `namespaceScoped` is an option if you are deploying only a single instance per cluster.

## Operator defaults

These are the current defaults for the operator:

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
# Clone operator project
$ git clone https://gitlab.com/frenchtoasters/zabbix-operator.git

# Change directory to zabbix-operator
$ cd zabbix-operator/zabbix-operator

# Create operator namespace
$ kubectl create ns operator

# Change diretory to operator
$ cd zabbix-operator/zabbix-operator

# Create custom resource definition
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_zabbixes_crd.yaml

# Create service account
$ kubectl create -f deploy/service_account.yaml

# Create role
$ kubectl create -f deploy/role.yaml

# Create role binding
$ kubectl create -f deploy/role_binding.yaml

# Deploy operator into cluster
$ kubectl create -f deploy/operator.yaml

# Create example default custom resource
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_v1alpha1_zabbix_cr.yaml
```

## Testing 

There are currently two ways of testing the operator, both require `minikube` running locally and `kubectl` working
without passing a `--kubeconfig` parameter. For rapid development the quickest way is to use the `ansible` testing
method. This runs the `zabbix-operator/roles/playbook.yml` using your local `python` environment. The other method is 
using the `operator-sdk` to run it locally, this method is a bit slower and requires a few extra terminals open. 

#### Test operator locally using ansible

```bash
# Start minikube instance
$ minikube start

# Clone operator project
$ git clone https://gitlab.com/frenchtoasters/zabbix-operator.git

# Create local virtual environment 
$ python -m virtualenv venv

# Activate environment
$ source venv/bin/active

# Install operator requirements
$ pip install -r requirements.txt

# Install anisble zabbix role
$ ansible-playbook zabbix-operator/roles/playbook.yml
```

#### Test operator locally using operator-sdk

```bash
# Start minikube instance
$ minikube start

# Clone operator project
$ git clone https://gitlab.com/frenchtoasters/zabbix-operator.git

# Change diretory to operator
$ cd zabbix-operator/zabbix-operator

# Create custom resource definition
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_zabbixes_crd.yaml

# Create service account
$ kubectl create -f deploy/service_account.yaml

# Create role
$ kubectl create -f deploy/role.yaml

# Create role binding
$ kubectl create -f deploy/role_binding.yaml

# Run operator locally using operator-sdk
$ operator-sdk run --local

# Create empty custom resource to create cluster with defaults
$ kubectl create -f deploy/crds/monitoring.frenchtoastman.com_v1alpha1_zabbix_cr.yaml 
```

## Known issues

* Labels do not update when changed in cr spec for: namespace, statefulset, deployment

### Build images

```bash
# build your workspace environment
$ docker build -t registry.gitlab.com/frenchtoasters/zabbix-operator/build:latest .

# build operator using operator-sdk
$ operator-sdk build registry.gitlab.com/frenchtoasters/zabbix-operator/zabbix-operator:latest

# build zabbix database image
$ docker build -t registry.gitlab.com/frenchtoasters/zabbix-operator/zabbix-database-postgres:latest -f zabbix-database/Dockerfile .
```

### Update database schema

```bash
$ docker run -it registry
```

### Release images

```bash
$ docker push registry.gitlab.com/frenchtoasters/zabbix-operator/build:latest
$ docker push registry.gitlab.com/frenchtoasters/zabbix-operator/zabbix-operator:latest
$ docker push registry.gitlab.com/frenchtoasters/zabbix-operator/zabbix-database-postgres:latest
```