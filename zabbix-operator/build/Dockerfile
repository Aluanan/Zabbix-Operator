FROM quay.io/operator-framework/ansible-operator:v0.17.0
LABEL maintainer="tylerfrench2@gmail.com"

COPY requirements.yml ${HOME}/requirements.yml
RUN ansible-galaxy collection install -r ${HOME}/requirements.yml \
 && chmod -R ug+rwx ${HOME}/.ansible

USER root
RUN dnf -y updateinfo && dnf -y install curl openssl
RUN curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
USER ansible-operator

COPY watches.yaml ${HOME}/watches.yaml

COPY roles/ ${HOME}/roles/
