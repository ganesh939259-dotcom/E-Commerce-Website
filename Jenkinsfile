pipeline {
    agent any

    stages {
        stage('Git Pull') {
            steps {
                sh 'git pull origin master'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }
}
