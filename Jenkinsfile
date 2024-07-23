pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = 'henpe36/django-app'
        EMAIL_RECIPIENTS = 'henpesin@gmail.com'
        APP_MACHINE_IP = '192.168.56.11'
        APP_MACHINE_USER = 'henpe'
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
                    docker.build("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}").inside {
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
                        docker.image("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy to App Machine') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                sshagent(['app-machine-credentials']) {
                    sh "ssh ${env.APP_MACHINE_USER}@${env.APP_MACHINE_IP} 'docker pull ${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER} && docker run -d -p 8000:8000 ${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}'"
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
