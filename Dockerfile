FROM docker.dbc.dk/dbc-python3

RUN useradd -m python
RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates gcc g++ git \
	curl tar bzip2 postgresql-client zip unzip make ssh
RUN apt-get install -y libnss-unknown

# libnss-unknown is installed to be able to use ssh with user id's not present
# in the docker container, such as when running the container from a jenkins pipeline.
# (For some reason you get id errors if installing it in the same command as e.g. ssh)

RUN pip install -U pip wheel twine deployversioner Sphinx dbc_pytools pyyaml requests pytest.xdist pytest-cov jsonpath-ng

COPY webservice_validation.py /usr/local/bin/webservice_validation.py

USER python
WORKDIR /home/python
