FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
  python3.6 \ 
  python3-pip \
  pkg-config \
  g++ \
  git \
  sudo \
  cmake \
  vim-common \
  libwebsockets-dev \
  libjson-c-dev \
  libssl-dev \
  sudo \
  systemd \
  openjdk-8-jdk \
  maven \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
 
  



WORKDIR /shell
RUN git clone https://github.com/tsl0922/ttyd.git
RUN cd ttyd && mkdir build && cd build && cmake .. && make && make install
EXPOSE 7681



WORKDIR /project
ADD . /project
RUN chmod +x ttyd.sh

RUN pip3 install -r requirements.txt
EXPOSE 5001

CMD ["sh","./ttyd.sh"]


