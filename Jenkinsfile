#!groovy

def workerNode = "xp-build-i01"

pipeline {
	agent {label workerNode}
	options {
		disableConcurrentBuilds()
	}
	environment {
		DOCKER_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
	}
	triggers {
		pollSCM("H/02 * * * *")
		upstream(upstreamProjects: "Docker-base-python3,ai/pyutils/master,ai/dbc-pytools/master",
			threshold: hudson.model.Result.SUCCESS)
	}
	stages {
		stage("test") {
			agent {
				docker {
					label workerNode
					image "docker-dbc.artifacts.dbccloud.dk/build-env"
					alwaysPull true
				}
			}
			steps {
				sh """#!/usr/bin/env bash
					set -xe
					rm -rf env
					python3 -m venv env
					source env/bin/activate
					pip install -U pip wheel
					cd webservice-validation
					pip install .
					python3 -m unittest discover -s tests
				"""
			}
		}
		stage("build") {
			steps {
				script {
					image = docker.build("build-env:${DOCKER_TAG}", "--no-cache --pull .")
                    docker.withRegistry("https://docker-dbc.artifacts.dbccloud.dk", "docker") {
                        image.push()
                        if (env.BRANCH_NAME ==~ /master|trunk/) {
                            image.push "latest"
                        }
					}
				}
			}
		}
	}
}
