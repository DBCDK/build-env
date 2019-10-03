FROM docker.dbc.dk/dbc-python3

RUN useradd -m python
RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates gcc g++ git curl tar

RUN pip install -U pip wheel twine
RUN pip install git+https://github.com/DBCDK/kube-deployment-auto-committer#egg=deployversioner

USER python
WORKDIR /home/python
