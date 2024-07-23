pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = 'henpe36/django-app'
        EMAIL_RECIPIENTS = 'henpesin@gmail.com'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Run Application Locally') {
            steps {
                script {
                    // Run the application locally
                    sh 'docker run -d --name local_app -p 8000:8000 ${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests against the local application
                    try {
                        sh 'docker exec local_app python manage.py test'
                    } finally {
                        // Always remove the local application container
                        sh 'docker rm -f local_app'
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
                script {
                    sshagent(['app-machine-credentials']) {
                        sh '''
                            ssh -o StrictHostKeyChecking=no vagrant@127.0.0.1 -p 2200 '
                            docker pull ${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER} &&
                            docker stop deployed_app || true &&
                            docker rm deployed_app || true &&
                            docker run -d --name deployed_app -p 8000:8000 ${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}'
                        '''
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
