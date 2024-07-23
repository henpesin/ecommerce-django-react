pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = 'henpe36/django-app'
        SSH_CREDENTIALS = credentials('app-machine-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/henpesin/ecommerce-django-react.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKERHUB_REPO}:latest")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}:latest").inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    docker.withRegistry('', 'dockerhub') {
                        docker.image("${env.DOCKERHUB_REPO}:latest").push()
                    }
                }
            }
        }

        stage('Test SSH Connection') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    sshagent(credentials: ['app-machine-credentials']) {
                        sh """
                        echo 'Testing SSH connection...'
                        ssh -o StrictHostKeyChecking=no henpe@192.168.56.11 echo 'SSH connection successful'
                        """
                    }
                }
            }
        }

        stage('Deploy to App Machine') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    sshagent(credentials: ['app-machine-credentials']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no henpe@192.168.56.11 << EOF
                        docker pull ${env.DOCKERHUB_REPO}:latest
                        docker stop django-app || true
                        docker rm django-app || true
                        docker run -d -p 8000:8000 --name django-app ${env.DOCKERHUB_REPO}:latest
                        EOF
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }

        always {
            archiveArtifacts artifacts: '**/reports/*.xml', allowEmptyArchive: true
            junit 'reports/**/*.xml'
        }
    }
}
