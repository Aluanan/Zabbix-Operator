FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y curl software-properties-common
RUN add-apt-repository -y ppa:rmescandon/yq && apt-get -y update && apt-get install -y yq && apt-get -y autoclean

# Install Kubectl latest
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl

# Install Helm 3.2.4
RUN curl -LO https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz && tar -zxvf helm-v3.2.4-linux-amd64.tar.gz && mv ./linux-amd64/helm /usr/local/bin/helm