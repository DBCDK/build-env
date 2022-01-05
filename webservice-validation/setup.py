#!/usr/bin/env python3

from setuptools import setup

setup(name="webservice-validation",
    version="1.0.0",
    package_dir={"": "src"},
    packages=["webservice_validation"],
    description="",
    provides=["webservice_validation"],
    install_requires=["jsonpath-ng", "requests", "rrflow", "pyyaml"],
    entry_points=
        {"console_scripts": [
            "webservice-validation = webservice_validation.webservice_validation:main",
        ]}
    )
