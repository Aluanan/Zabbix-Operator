FROM ubuntu:latest

LABEL maintainer="tylerfrench2@gmail.com"

# Set working directory
WORKDIR /opt/operator

# Set operator-sdk version
ENV RELEASE_VERSION v0.17.0

# Install local deps
RUN apt-get update && apt-get install -y curl gpg

# Copy operator-sdk install script to container
COPY install-operator-sdk.sh /opt/operator

# Run install script
RUN /opt/operator/install-operator-sdk.sh