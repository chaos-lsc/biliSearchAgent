FROM nvcr.io/nvidia/pytorch:24.01-py3

# set WORKDIR
WORKDIR /workspace/biliAgent

# setup environment
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# replace mirror
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse\n" > /etc/apt/sources.list && \
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse\n" >> /etc/apt/sources.list && \
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse\n" >> /etc/apt/sources.list && \
  echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse\n" >> /etc/apt/sources.list

# dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 zip \
 unzip \
 make \
 git 

# change pip mirror
RUN python -m \
# pip install --upgrade pip \
# &&\
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# pip install requirements
# COPY requirement.txt .
# RUN pip install -r requirement.txt

ENV NVIDIA_VISIBLE_DEVICES=all NVIDIA_DRIVER_CAPABILITIES=all

