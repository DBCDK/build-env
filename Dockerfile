FROM docker.dbc.dk/dbc-python3

RUN useradd -m python
RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates gcc g++ git curl tar bzip2 postgresql-client

RUN pip install -U pip wheel twine deployversioner Sphinx dbc_pytools pyyaml requests pytest.xdist

COPY webservice_validation.py /usr/local/bin/webservice_validation.py

USER python
WORKDIR /home/python
