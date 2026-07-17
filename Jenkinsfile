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

        stage('生成 Allure 报告') {
            steps {
                bat 'allure generate ./reports --clean -o ./allure-report'
            }
        }
    }

    post {
    always {
        junit 'reports/junit.xml'
        publishHTML([
            reportDir: './allure-report',
            reportFiles: 'index.html',
            reportName: 'Allure Report',
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: false
        ])
    }
}
}