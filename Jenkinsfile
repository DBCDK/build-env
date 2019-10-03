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
					image = docker.build("docker.dbc.dk/build-env:${DOCKER_TAG}", "--no-cache .")
					image.push()
					if(env.BRANCH_NAME == "master") {
						image.push("latest")
					}
				}
			}
		}
	}
}
