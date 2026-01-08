pipeline {
    agent any

    environment {
        IMAGE_NAME = "feature-test-service"
        IMAGE_TAG  = "latest"
        DOCKER_REGISTRY = "docker.io/saiprasad361"
        K8S_NAMESPACE = "default"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build Image with Kaniko') {
            steps {
                container('kaniko') {
                    sh '''
                      echo "Building image using Kaniko"
                      /kaniko/executor \
                        --context $PWD \
                        --dockerfile Dockerfile \
                        --destination ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                        --cache=true
                    '''
                }
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
                  kubectl rollout status deployment/feature-test-service \
                    -n ${K8S_NAMESPACE}
                '''
            }
        }

        stage('Run Feature & Bug-Fix Tests') {
            steps {
                sh '''
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
            echo "✅ Pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}

