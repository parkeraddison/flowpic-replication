# For code development

FROM jupyter/scipy-notebook:latest

USER root

### Network-stats requirements
#
# libpcap is needed by pcapy
RUN apt-get update && \
    apt-get install -y \
    libpcap-dev

WORKDIR /usr/local/src

# Get pcapy source and install
RUN wget "https://github.com/helpsystems/pcapy/archive/0.11.5.tar.gz" && \
    tar -xf 0.11.5.tar.gz && \
    rm 0.11.5.tar.gz

RUN cd pcapy*/ && \
    python3 setup.py install

# Get impacket source and install
RUN wget "https://github.com/SecureAuthCorp/impacket/releases/download/impacket_0_9_21/impacket-0.9.21.tar.gz" && \
    tar -xf impacket*.tar.gz && \
    rm impacket*.tar.gz

RUN cd impacket*/ && \
    pip3 install .

### Development requirements
#
# (none yet that aren't already covered in base image)
# RUN ...

### DSMLP requirements
#
# We need to have the run_jupyter.sh file in our root directory otherwise
# DSMLP gets angry if we try launching the image with any `launch-*.sh`
WORKDIR /
RUN wget https://raw.githubusercontent.com/ucsd-ets/datahub-base-notebook/master/scripts/run_jupyter.sh && \
    chmod +x run_jupyter.sh

### Final setup steps
#
# Environment specified in base image.
USER $NB_UID
WORKDIR $HOME

# Get our respository in there
RUN git clone https://github.com/parkeraddison/data-science-capstone.git
WORKDIR $HOME/data-science-capstone

LABEL maintainer="Parker Addison <pgaddiso@ucsd.edu>"
