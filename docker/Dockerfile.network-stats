FROM debian:buster

### Install apt dependencies for running network-stats
RUN apt-get update && \
    apt-get install -y \
    git \
    libpcap-dev \
    python3 \
    python3-pip \
    wget

### Install non-apt dependencies for running network-stats
WORKDIR /usr/local/src

# Get impacket source
RUN wget "https://github.com/SecureAuthCorp/impacket/releases/download/impacket_0_9_21/impacket-0.9.21.tar.gz" && \
    tar -xf impacket*.tar.gz && \
    rm impacket*.tar.gz

# Install impacket
RUN cd impacket*/ && \
    pip3 install .

# Get the pcapy source
RUN wget "https://github.com/helpsystems/pcapy/archive/0.11.5.tar.gz" && \
    tar -xf 0.11.5.tar.gz && \
    rm 0.11.5.tar.gz

# Install pcapy
RUN cd pcapy*/ && \
    python3 setup.py install

###

WORKDIR /home

RUN git clone "https://github.com/viasat/network-stats.git"

CMD ["bash"]
