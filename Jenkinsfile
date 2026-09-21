pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Pipeline') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'postgres-db',
                        usernameVariable: 'POSTGRES_USER',
                        passwordVariable: 'POSTGRES_PASSWORD'
                    )
                ]) {
                    bat 'python main.py'
                }
            }
        }

    }
}