FROM python:3.12-slim

RUN apt-get -q -y update 
RUN apt-get install -y gcc

ENV USERNAME=uploadit
ENV WORKING_DIR=/home/uploadit

WORKDIR ${WORKING_DIR}

COPY uploadit uploadit
COPY requirements.txt .
COPY service_entrypoint.sh .

RUN groupadd ${USERNAME} && useradd -g ${USERNAME} ${USERNAME}

RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
RUN chmod -R u=rwx,g=rwx ${WORKING_DIR}

USER ${USERNAME}
ENV PATH "$PATH:/home/${USERNAME}/.local/bin"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=uploadit:serve

RUN chmod +x service_entrypoint.sh

EXPOSE 5000
RUN flask db init

ENTRYPOINT [ "./service_entrypoint.sh" ]
