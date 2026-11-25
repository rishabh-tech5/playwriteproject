pipeline {
  // This pipeline uses PowerShell and Windows paths, so the selected agent must be Windows.
  agent any

  options {
    timestamps()
    timeout(time: 60, unit: 'MINUTES')
  }

  parameters {
    choice(
      name: 'TEST_SUITE',
      choices: ['all', 'test', 'first_test', 'test_sample', 'recording'],
      description: 'Select the test suite to run'
    )
    choice(
      name: 'BROWSER',
      choices: ['chromium', 'firefox', 'webkit'],
      description: 'Select the browser'
    )
    choice(
      name: 'MODE',
      choices: ['headless', 'headed'],
      description: 'Headed mode needs an interactive Windows desktop'
    )
    booleanParam(
      name: 'INSTALL_DEPS',
      defaultValue: true,
      description: 'Install Python dependencies and Playwright browsers'
    )
  }

  environment {
    CI = 'true'
    PLAYWRIGHT_BROWSERS_PATH = '0'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Environment') {
      steps {
        powershell '''
          if (-not (Test-Path "venv\\Scripts\\python.exe")) {
            python -m venv venv
          }

          if ($env:INSTALL_DEPS -eq "true") {
            & .\\venv\\Scripts\\python.exe -m pip install pytest playwright pytest-playwright pytest-html

            if (Test-Path "requirements.txt") {
              & .\\venv\\Scripts\\python.exe -m pip install -r requirements.txt
            }
          }
        '''
      }
    }

    stage('Install Playwright Browsers') {
      when {
        expression { params.INSTALL_DEPS }
      }
      steps {
        powershell '''
          & .\\venv\\Scripts\\python.exe -m playwright install
        '''
      }
    }

    stage('Run Playwright Tests') {
      steps {
        script {
          def testPath
          switch (params.TEST_SUITE) {
            case 'all':
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

          def modeArg = params.MODE == 'headed' ? '--headed' : ''

          powershell """
            if (Test-Path "reports") {
              Remove-Item -Recurse -Force "reports"
            }
            New-Item -ItemType Directory -Force "reports" | Out-Null

            & .\\\\venv\\\\Scripts\\\\python.exe -m pytest '${testPath}' `
              --browser='${params.BROWSER}' `
              ${modeArg} `
              --html="reports/report_${params.BROWSER}_${env.BUILD_NUMBER}.html" `
              --self-contained-html `
              --junitxml="reports/results_${params.BROWSER}_${env.BUILD_NUMBER}.xml" `
              -v
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
          <p><a href="${env.BUILD_URL}">Open Jenkins Build</a></p>
        """,
        to: "rishabhrathaur65@gmail.com",
        from: "nishantgupta3044@gmail.com",
        replyTo: "rishabhrathaur65@gmail.com",
        mimeType: 'text/html'
      )
    }

    failure {
      powershell '''
        New-Item -ItemType Directory -Force "reports" | Out-Null

        if (Test-Path "test-results") {
          Get-ChildItem -Path "test-results" | ForEach-Object {
            Copy-Item $_.FullName -Destination "reports/" -Recurse -Force
          }
        }
      '''
    }
  }
}