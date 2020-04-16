
FROM ubuntu:18.04

MAINTAINER "Markus Näther <naetherm@informatik.uni-freiburg.de>"

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-dev python3-pip

RUN mkdir /code/
COPY . /code/
WORKDIR /code/

RUN pip3 install -r requirements.txt

RUN ls -la

CMD ["/bin/bash"]

ENTRYPOINT ["./run.sh"]
