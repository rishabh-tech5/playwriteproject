// Jenkinsfile.windows
// Declarative Jenkins pipeline for Windows build agents - Python Playwright Project

/*
Pipeline Stages:
1. Checkout: Checks out the source code from the repository.
2. Setup Python Environment: Creates/activates virtual environment and installs dependencies.
3. Install Playwright Browsers: Installs Playwright browsers and dependencies.
4. Run Playwright Tests: Executes the selected test suite with specified browser and mode.
5. Post Actions: Archives test reports, publishes JUnit and HTML reports.
6. Email Notification: Sends email notification with build status and report links.
7. Parameters: Allows users to select test suite, browser, and mode.
*/

pipeline {
  agent any
  tools {
    git 'Default'
  }
  options {
    timestamps()
    timeout(time: 60, unit: 'MINUTES')
  }
  parameters {
    choice(
      name: 'TEST_SUITE',
      choices: ['all', 'test', 'first_test', 'test_sample', 'recording'],
      description: 'Select the test suite/file to run (all = all tests in test/ folder)'
    )
    choice(
      name: 'BROWSER',
      choices: ['chromium', 'firefox', 'webkit'],
      description: 'Select the browser for tests'
    )
    choice(
      name: 'MODE',
      choices: ['headed', 'headless'],
      description: 'Run tests in headed or headless mode'
    )
    booleanParam(
      name: 'INSTALL_DEPS',
      defaultValue: true,
      description: 'Install/update Python dependencies and Playwright browsers'
    )
  }
  environment {
    PYTHON_ENV = 'test'
    CI = 'true'
    PLAYWRIGHT_BROWSERS_PATH = '0'
  }
  stages {
    stage('🔄 Checkout') {
      steps {
        checkout scm
      }
    }
    stage('🐍 Setup Python Environment') {
      steps {
        script {
          if (params.INSTALL_DEPS) {
            // Create virtual environment if it doesn't exist
            powershell '''
              if (-not (Test-Path "venv")) {
                python -m venv venv
              }
              .\\venv\\Scripts\\Activate.ps1
              python -m pip install --upgrade pip
              pip install pytest playwright pytest-playwright pytest-html
            '''
            // Install project dependencies if requirements.txt exists
            powershell '''
              if (Test-Path "requirements.txt") {
                .\\venv\\Scripts\\Activate.ps1
                pip install -r requirements.txt
              }
            '''
          }
        }
      }
    }
    stage('🤖 Install Playwright Browsers') {
      steps {
        script {
          if (params.INSTALL_DEPS) {
            powershell '''
              .\\venv\\Scripts\\Activate.ps1
              playwright install --with-deps
            '''
          }
        }
      }
    }
    stage('▶️ Run Playwright Tests') {
      steps {
        script {
          def testPath = ''
          def browserArg = "--browser=${params.BROWSER}"
          def modeArg = params.MODE == 'headed' ? '--headed' : '--headless'
          def htmlReport = "--html=reports/report_${params.BROWSER}_${BUILD_NUMBER}.html --self-contained-html"
          def junitReport = "--junitxml=reports/results_${params.BROWSER}_${BUILD_NUMBER}.xml"

          switch(params.TEST_SUITE) {
            case 'all':
              testPath = 'test/'
              break
            case 'test':
              testPath = 'test/'
              break
            case 'first_test':
              testPath = 'first_test.py'
              break
            case 'test_sample':
              testPath = 'test_sample.py'
              break
            case 'recording':
              testPath = 'test/recording.py'
              break
            default:
              testPath = 'test/'
          }

          powershell """
            .\\venv\\Scripts\\Activate.ps1
            pytest ${testPath} ${browserArg} ${modeArg} ${htmlReport} ${junitReport} -v
          """
        }
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
      junit testResults: 'reports/results_*.xml', allowEmptyResults: true
      publishHTML([
        allowMissing: true,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'reports',
        reportFiles: 'report_*.html',
        reportName: 'Playwright HTML Report'
      ])
      emailext(
        subject: "Jenkins Build: ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
        body: """
            <h2>Playwright Test Execution Report</h2>
            <p><b>Job:</b> ${env.JOB_NAME}</p>
            <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
            <p><b>Status:</b> ${currentBuild.currentResult}</p>
            <p><b>Test Suite:</b> ${params.TEST_SUITE}</p>
            <p><b>Browser:</b> ${params.BROWSER}</p>
            <p><b>Mode:</b> ${params.MODE}</p>
            <p>
              <a href="${env.BUILD_URL}">Open Jenkins Build</a> |
              <a href="${env.BUILD_URL}Playwright_20HTML_20Report">Open Playwright HTML Report</a>
            </p>
        """,
        to: "rishabhrathaur65@gmail.com",
        from: "nishantgupta3044@gmail.com",
        replyTo: "rishabhrathaur65@gmail.com",
        mimeType: "text/html"
      )
    }
    success {
      script {
        powershell 'Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue'
      }
    }
    failure {
      script {
        powershell '''
          .\\venv\\Scripts\\Activate.ps1
          # Capture screenshots on failure if any
          Get-ChildItem -Path "test-results" -ErrorAction SilentlyContinue | ForEach-Object {
            Copy-Item $_.FullName -Destination "reports/" -Force
          }
        '''
      }
    }
  }
}