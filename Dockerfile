FROM fedora:26

ENV PATH="/usr/lib/python3.6/site-packages:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN dnf -y update && dnf clean all
RUN dnf install -y libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel
RUN dnf install -y pkg-config gcc-c++
RUN dnf install -y redhat-rpm-config
RUN dnf install -y python3-devel

RUN dnf -y install which
RUN pip3 install tox
RUN pip3 install coveralls
