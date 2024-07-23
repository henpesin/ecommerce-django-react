pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = 'henpe36/django-app'
        SSH_CREDENTIALS = credentials('jenkins-key')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
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
            steps {
                script {
                    sshagent(credentials: ['jenkins-key']) {
                        sh """
                        echo Testing SSH connection...
                        ssh -o StrictHostKeyChecking=no vagrant@192.168.56.11 echo SSH connection successful
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
                    sshagent(credentials: ['jenkins-key']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no vagrant@192.168.56.11 'bash -s' <<-'ENDSSH'
                            docker pull ${env.DOCKERHUB_REPO}:latest
                            docker stop django-app || true
                            docker rm django-app || true
                            docker run -d -p 8000:8000 --name django-app ${env.DOCKERHUB_REPO}:latest
                        ENDSSH
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
