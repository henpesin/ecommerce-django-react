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
                git branch: 'main', url: 'https://github.com/henpesin/ecommerce-django-react.git'
            }
        }

        // stage('Build Locally') {
        //     steps {
        //         sh '''
        //         echo "Installing dependencies using apt..."
        //         sudo apt-get update -y
        //         sudo apt-get install -y python3 python3-pip python3-venv

        //         echo "Installing Node.js..."
        //         curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
        //         sudo apt-get install -y nodejs

        //         echo "Setting up virtual environment and installing dependencies..."
        //         python3 -m venv .venv
        //         . .venv/bin/activate
        //         pip install --upgrade pip
        //         pip install -r requirements.txt

        //         echo "Building frontend..."
        //         cd frontend
        //         npm install
        //         npm run build
        //         cd ..

        //         echo "Running database migrations..."
        //         .venv/bin/python manage.py makemigrations
        //         .venv/bin/python manage.py migrate

        //         echo "Collecting static files..."
        //         .venv/bin/python manage.py collectstatic --noinput

        //         echo "Starting Django development server..."
        //         nohup .venv/bin/python manage.py runserver 0.0.0.0:8000 &
        //         '''
        //     }
        // }

        // stage('Test Locally') {
        //     steps {
        //         script {
        //             catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
        //                 sh '''
        //                 echo "Activating virtual environment..."
        //                 . .venv/bin/activate

        //                 echo "Running tests..."
        //                 pytest --html=reports/report.html
        //                 '''
        //             }
        //         }
        //     }
        // }

        // stage('Publish Report') {
        //     steps {
        //         publishHTML(target: [
        //             allowMissing: false,
        //             alwaysLinkToLastBuild: true,
        //             keepAll: true,
        //             reportDir: 'reports',
        //             reportFiles: 'report.html',
        //             reportName: 'Test Report',
        //             reportTitles: 'Test Report'
        //         ])
        //     }
        // }

        // stage('Build Docker Image') {
        //     when {
        //         expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
        //     }
        //     steps {
        //         script {
        //             docker.build("${env.DOCKERHUB_REPO}:latest")
        //         }
        //     }
        // }

        // stage('Push Docker Image') {
        //     when {
        //         expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
        //     }
        //     steps {
        //         script {
        //             docker.withRegistry('', 'dockerhub') {
        //                 docker.image("${env.DOCKERHUB_REPO}:latest").push()
        //             }
        //         }
        //     }
        // }

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
                            ssh -o StrictHostKeyChecking=no vagrant@192.168.56.11 '
                            docker pull ${env.DOCKERHUB_REPO}:latest
                            docker stop django-app || true
                            docker rm django-app || true
                            docker run -d -p 8000:8000 --name django-app ${env.DOCKERHUB_REPO}:latest
                            '
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
            archiveArtifacts artifacts: '**/reports/report.html', allowEmptyArchive: true
        }
    }
}
