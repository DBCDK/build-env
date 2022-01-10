FROM docker.dbc.dk/dbc-python3

RUN useradd -m python
RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates gcc g++ git \
	curl tar bzip2 postgresql-client zip unzip make ssh
RUN apt-get install -y libnss-unknown

# libnss-unknown is installed to be able to use ssh with user id's not present
# in the docker container, such as when running the container from a jenkins pipeline.
# (For some reason you get id errors if installing it in the same command as e.g. ssh)

RUN pip install -U pip wheel twine deployversioner Sphinx dbc_pytools pyyaml requests pytest.xdist pytest-cov

# The cargo directory must be writable for all users who are going to build since that's where cargo stores downloaded packages.
RUN mkdir /rust && chmod 777 /rust
ENV RUSTUP_HOME=/rust
ENV CARGO_HOME=/rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup.sh && \
	sh ./rustup.sh -y
ENV PATH=/rust/bin:$PATH

COPY webservice-validation webservice-validation
RUN cd webservice-validation && \
	pip install .

RUN curl -L https://artifactory.dbc.dk/artifactory/ai-generic/kube-tools-rs/kube-tools -o /usr/local/bin/kube-tools && \
	chmod 755 /usr/local/bin/kube-tools

USER python
WORKDIR /home/python
