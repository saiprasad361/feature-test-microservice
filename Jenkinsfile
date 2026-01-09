pipeline {
    agent any

    environment {
        IMAGE_NAME = "saiprasad361/feature-test-service"
        IMAGE_TAG  = "latest"
        K8S_NAMESPACE = "default"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push Image (Kaniko)') {
            steps {
                container('kaniko') {
                    sh '''
                      echo "Building and pushing Docker image"
                      /kaniko/executor \
                        --context $PWD \
                        --dockerfile Dockerfile \
                        --destination docker.io/${IMAGE_NAME}:${IMAGE_TAG} \
                        --cache=true
                    '''
                }
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

        stage('Verify Deployment') {
            steps {
                sh '''
                  kubectl rollout status deployment/feature-test-service \
                    -n ${K8S_NAMESPACE}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Image built, pushed, and deployed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}

