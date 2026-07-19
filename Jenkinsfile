pipeline {
    agent any

    environment {
        PYTHON = 'D:\\python38\\python.exe'
        // 设置 Playwright 浏览器下载路径（避免缓存问题）
        PLAYWRIGHT_BROWSERS_PATH = '0'
    }

    stages {
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('安装依赖') {
            steps {
                bat "${PYTHON} -m pip install -r requirements.txt"
                // 安装 Playwright 浏览器（CI 环境必需）
                bat 'playwright install chromium'
            }
        }

        stage('运行接口测试') {
            steps {
                bat "${PYTHON} -m pytest testcases/test_main.py testcases/test_products.py testcases/test_cart.py testcases/test_order.py --alluredir=./reports/api --junitxml=./reports/junit.xml || exit 0"
            }
        }

        stage('运行 UI 测试') {
            steps {
                bat "${PYTHON} -m pytest testcases/test_ui_login.py --alluredir=./reports/ui || exit 0"
            }
        }

        stage('合并 Allure 报告') {
            steps {
                // 合并两个报告目录（接口测试和 UI 测试）
                bat 'allure generate ./reports/api ./reports/ui --clean -o ./allure-report || echo "Allure generate failed"'
            }
        }
    }

    post {
        always {
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