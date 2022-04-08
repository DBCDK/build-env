#!groovy

def workerNode = "xp-build-i01"

pipeline {
	agent {label workerNode}
	environment {
		DOCKER_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
	}
	triggers {
		pollSCM("H/02 * * * *")
		upstream(upstreamProjects: "Docker-base-python3",
			threshold: hudson.model.Result.SUCCESS)
	}
	stages {
		stage("test") {
			agent {
				docker {
					label workerNode
					image "docker.dbc.dk/build-env"
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
					image = docker.build("docker-dbc.artifacts.dbccloud.dk/build-env:${DOCKER_TAG}", "--no-cache --pull .")
					image.push()
					if(env.BRANCH_NAME == "master") {
						image.push("latest")
					}
				}
			}
		}
	}
}
