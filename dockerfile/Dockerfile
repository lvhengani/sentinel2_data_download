FROM lvhengani/p3gdal:latest

LABEL maintainer Lufuno Vhengani <lvhengani@csir.co.za>

ARG DEBIAN_FRONTEND=noninteractive
ARG GOSU_VERSION=1.10
ARG GDAL_VERSION=2.1.4
ARG SEN2COR_VERSION=02.08.00
ARG SEN2COR_DIRECTORY=2.8.0
ARG SEN2COR="Sen2Cor-${SEN2COR_VERSION}-Linux64.run" 
ADD requirements /requirements
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
        build-essential \
        python3-dev \
        gcc \
        unzip \
        curl \
        wget
RUN pip3 install -U -r /requirements
RUN wget "http://step.esa.int/thirdparties/sen2cor/${SEN2COR_DIRECTORY}/${SEN2COR}" && \
    bash ${SEN2COR} && \
    rm ${SEN2COR}  
RUN curl -o /usr/local/bin/gosu -sSL "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-amd64" && \
    chmod +x /usr/local/bin/gosu && \
    chmod +x /docker-entrypoint.sh && \  
    apt-get remove -y build-essential python3-dev