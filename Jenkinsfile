pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('安装依赖') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('运行测试') {
            steps {
                bat 'pytest testcases/ --alluredir=./reports'
            }
        }
    }

    post {
        always {
            allure results: [[path: 'reports']]
        }
    }
}