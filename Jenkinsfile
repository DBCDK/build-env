#!groovy

def workerNode = "devel8"

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
		stage("build") {
			steps {
				script {
					image = docker.build("docker-io.dbc.dk/python3-build-image:${DOCKER_TAG}")
					image.push()
				}
			}
		}
	}
}
