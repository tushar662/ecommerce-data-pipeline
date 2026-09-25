pipeline {
    agent any

    environment {
        DB_HOST = 'localhost'
        DB_PORT = '5433'
        DB_NAME = 'ecommerce_db'
        DB_USER = 'postgres'
    }

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest'
            }
        }

        stage('Run Pipeline') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'postgres-db',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'POSTGRES_PASSWORD'
                    )
                ]) {
                    bat 'python main.py'
                }
            }
        }

    }
}