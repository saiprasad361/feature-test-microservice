pipeline {
    agent { label 'podman-agent' }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = "feature-test-service"
        IMAGE_TAG  = "latest"
        K8S_NAMESPACE = "default"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build Image with Podman') {
            steps {
                sh '''
                  echo "Using Podman to build image"
                  podman version
                  podman build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                  echo "Deploying application to Kubernetes"
                  kubectl apply -f k8s/deployment.yaml
                  kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Wait for Pods') {
            steps {
                sh '''
                  echo "Waiting for deployment rollout"
                  kubectl rollout status deployment/feature-test-service \
                    -n ${K8S_NAMESPACE}
                '''
            }
        }

        stage('Run Feature & Bug-Fix Tests') {
            steps {
                sh '''
                  echo "Running API validation tests"
                  SERVICE_IP=$(kubectl get svc feature-test-service \
                    -n ${K8S_NAMESPACE} \
                    -o jsonpath='{.spec.clusterIP}')

                  ./tests/api_tests.sh http://${SERVICE_IP}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Podman-based pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed – check logs"
        }
    }
}

