pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build('postgres:latest', 'C:/Users/Wojtek/PycharmProjects/Hitchhiking_app/database')
                    docker.build('hitchhiking_app-app1:latest', 'C:/Users/Wojtek/PycharmProjects/Hitchhiking_app/app')
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    bat "docker network create hitchhiking-network"
                    bat "docker run -d --name container_app --network hitchhiking-network -p 5000:5000 hitchhiking_app-app1:latest"
                    bat 'ping 127.0.0.1 -n 10 > nul'
                    bat "docker run -d --name container_db --network hitchhiking-network -p 5432:5432 postgres:latest"
                    bat 'ping 127.0.0.1 -n 10 > nul'
                    bat "docker exec container_app python test_script.py"
                }
            }
        }
    }
    post {
        always {
            script {
                bat "call C:/Users/Wojtek/PycharmProjects/Hitchhiking_app/docker-clear.bat"
            }
        }
    }
}