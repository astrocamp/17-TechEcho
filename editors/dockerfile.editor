FROM python:3.9-slim

# inlcudes cpp, node.js, java
RUN apt-get update && \
    apt-get install -y gcc g++ make curl default-jdk && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

WORKDIR /code
