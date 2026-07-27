pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/cskarthi2752/contact-book-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t contact-book-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f contact-book-app || true
                docker run -d --name contact-book-app -p 5000:5000 contact-book-app
                '''
            }
        }
    }
}
