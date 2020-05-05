FROM centos:8 as builder

# Install package to grab database that can be upgraded to latest
RUN rpm -Uvh https://repo.zabbix.com/zabbix/4.5/rhel/8/x86_64/zabbix-release-4.5-2.el8.noarch.rpm
RUN dnf clean all
RUN dnf install -y zabbix-server-pgsql

FROM ubuntu:latest

LABEL maintainer="tylerfrench2@gmail.com"

# Set working directory
WORKDIR /opt/operator

# Set operator-sdk version
ENV RELEASE_VERSION=v0.17.0
ENV TZ=America/Kentucky/Louisville
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install local deps
RUN apt update && apt-get install -y curl gpg

# Copy operator-sdk install script to container
COPY install-operator-sdk.sh /opt/operator

# Run install script
RUN /opt/operator/install-operator-sdk.sh

# Move schema
COPY --from=builder /usr/share/doc/zabbix-server-pgsql/create.sql.gz /opt/operator/zabbix-schema-5.sql.gz