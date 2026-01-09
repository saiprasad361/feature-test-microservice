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

        stage('Build Docker Image (LOCAL ONLY)') {
            steps {
                sh '''
                  echo "Building Docker image locally (no push)"
                  docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                  echo "Deploying to Kubernetes using local image"
                  kubectl apply -f k8s/deployment.yaml
                  kubectl rollout restart deployment/feature-test-service
                '''
            }
        }

        stage('Verify Pods') {
            steps {
                sh '''
                  echo "Waiting for pods to become Ready"
                  kubectl rollout status deployment/feature-test-service \
                    -n ${NAMESPACE} --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Microservice is running successfully on Kubernetes"
        }
        failure {
            echo "❌ Deployment failed or pods not ready"
        }
    }
}

