pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = 'henpe36/django-app'
        EMAIL_RECIPIENTS = 'henpesin@gmail.com'
        SSH_CREDENTIALS = credentials('app-machine-credentials')
        DJANGO_SETTINGS_MODULE = 'backend.settings'
        SECRET_KEY = credentials('django-secret-key')
        DEBUG = 'True'  // Set to 'False' for production
        ALLOWED_HOSTS = 'localhost,127.0.0.1,192.168.56.11'
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
            mail to: "${env.EMAIL_RECIPIENTS}",
                 subject: "Jenkins Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}",
                 body: "The build ${env.BUILD_NUMBER} of job ${env.JOB_NAME} failed. Please check the console output for more details: ${env.BUILD_URL}"
        }

        always {
            archiveArtifacts artifacts: '**/reports/*.xml', allowEmptyArchive: true
            junit 'reports/**/*.xml'
        }
    }
}
