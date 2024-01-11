pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    bat 'ansible-playbook -i hosts.ini build.yml'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    bat 'ansible-playbook -i hosts.ini test.yml'
                }
            }
        }
    }
    post {
        always {
            script {
                bat 'ansible-playbook -i hosts.ini cleanup.yml'
            }
        }
    }
}