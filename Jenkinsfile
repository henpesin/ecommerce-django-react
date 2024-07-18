pipeline {
    agent any

    environment {
        // Define your environment variables here
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = 'henpe36/django-app'
        GIT_REPO = 'https://github.com/henpesin/ecommerce-django-react.git'
        GIT_BRANCH = 'main'
        EMAIL_RECIPIENTS = 'henpesin@gmail.com'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                git branch: "${env.GIT_BRANCH}", url: "${env.GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKERHUB_REPO}:${env.GIT_BRANCH}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}:${env.GIT_BRANCH}").inside {
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
                        docker.image("${env.DOCKERHUB_REPO}:${env.GIT_BRANCH}").push()
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}:${env.GIT_BRANCH}").run('-p 8000:8000')
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
