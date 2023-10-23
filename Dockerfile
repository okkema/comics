FROM python:3.11-bullseye as build
COPY ./ ./
RUN ./install.sh
ENTRYPOINT [ "python", "omnibus.py" ]
