pipeline {
    agent any

    environment {
        IMAGE_NAME = "feature-test-service"
        NAMESPACE = "default"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  docker build -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                  kubectl apply -f k8s/deployment.yaml
                  kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Wait for Pods') {
            steps {
                sh '''
                  kubectl rollout status deployment/feature-test-service
                '''
            }
        }

        stage('Run Feature & Bug Fix Tests') {
            steps {
                sh '''
                  SERVICE_IP=$(kubectl get svc feature-test-service \
                    -o jsonpath='{.spec.clusterIP}')
                  ./tests/api_tests.sh http://$SERVICE_IP
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Feature & bug-fix validation successful"
        }
        failure {
            echo "❌ Validation failed – investigate logs"
        }
    }
}

