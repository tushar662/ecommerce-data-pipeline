pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Extract Data') {
            steps {
                bat 'python src/extract.py'
            }
        }

    }
}