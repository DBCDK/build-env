FROM docker.dbc.dk/dbc-python3

RUN useradd -m python
RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates gcc g++ git curl tar

RUN pip install -U pip wheel twine deployversioner Sphinx dbc_pytools pyyaml requests

COPY simple_validation.py /usr/local/bin/simple_validation.py

USER python
WORKDIR /home/python
