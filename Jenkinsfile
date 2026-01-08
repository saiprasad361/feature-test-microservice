pipeline {
    agent {
        kubernetes {
            namespace 'cloudbees-builds'
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker/config.json
      subPath: .dockerconfigjson
    - name: workspace-volume
      mountPath: /workspace
  volumes:
  - name: docker-config
    secret:
      secretName: dockerhub-sai
  - name: workspace-volume
    emptyDir: {}
"""
        }
    }

    environment {
        IMAGE_NAME = "feature-test-service"
        IMAGE_TAG  = "latest"
        DOCKER_REPO = "docker.io/saiprasad361"
        K8S_NAMESPACE = "default"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push Image (Kaniko)') {
            steps {
                container('kaniko') {
                    sh '''
                      echo "Building and pushing image using my own Docker Hub credentials"
                      /kaniko/executor \
                        --context $PWD \
                        --dockerfile Dockerfile \
                        --destination ${DOCKER_REPO}/${IMAGE_NAME}:${IMAGE_TAG} \
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
            echo "✅ Image pushed using my Docker Hub credentials"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}

