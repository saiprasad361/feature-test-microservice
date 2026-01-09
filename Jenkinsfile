pipeline {
    agent any

    environment {
        IMAGE_NAME = "feature-test-service"
        IMAGE_TAG  = "local"
        NAMESPACE  = "default"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image with Podman (LOCAL)') {
            steps {
                sh '''
                  echo "Building image using Podman (no push)"
                  podman build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                  echo "Deploying to Kubernetes using local Podman image"
                  kubectl apply -f k8s/deployment.yaml
                  kubectl rollout restart deployment/feature-test-service
                '''
            }
        }

        stage('Verify Pods') {
            steps {
                sh '''
                  echo "Verifying pod readiness"
                  kubectl rollout status deployment/feature-test-service \
                    -n ${NAMESPACE} --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Image built with Podman and microservice is running on Kubernetes"
        }
        failure {
            echo "❌ Build or deployment failed"
        }
    }
}

