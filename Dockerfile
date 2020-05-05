FROM alpine:latest as builder
# Install local deps
WORKDIR /opt/build
RUN apk update && apk add --no-cache curl

# Get the latest link https://www.zabbix.com/download_sources#tab:pre-release
RUN curl -LO https://cdn.zabbix.com/development/5.0.0beta2/zabbix-5.0.0beta2.tar.gz
RUN tar -zxvf /opt/build/zabbix-5.0.0beta2.tar.gz
RUN cat /opt/build/zabbix-5.0.0beta2/database/postgresql/schema.sql /opt/build/zabbix-5.0.0beta2/database/postgresql/data.sql >> /opt/build/zabbix-create-5.sql

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

# Move schema
COPY --from=builder /opt/build/zabbix-create-5.sql /opt/operator/zabbix-schame-5.sql

# Copy operator-sdk install script to container
COPY install-operator-sdk.sh /opt/operator

# Run install script
RUN /opt/operator/install-operator-sdk.sh