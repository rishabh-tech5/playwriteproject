# Playwright Python Test Project - Jenkins Pipeline

This project uses **Python + pytest + Playwright** for end-to-end testing. The Jenkins pipeline is configured to run on Windows build agents.

## Project Structure

```
playwriteproject/
├── Jenkinsfile                 # Main Jenkins pipeline (copy of Jenkinsfile.windows)
├── Jenkinsfile.windows         # Windows-specific Jenkins pipeline
├── requirements.txt            # Python dependencies
├── pytest.ini                  # pytest configuration
├── conftest.py                 # pytest fixtures and configuration
├── .env.example                # Environment variables template
├── first_test.py               # Sample test file
├── test_sample.py              # Another sample test
├── test/
│   └── recording.py            # Recorded test
├── pages/                      # Page objects (empty - add your POMs here)
├── utils/                      # Utility functions (empty - add helpers here)
├── reports/                    # Test reports (generated)
└── venv/                       # Python virtual environment (created by pipeline)
```

## Jenkins Pipeline Parameters

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `TEST_SUITE` | `all`, `test`, `first_test`, `test_sample`, `recording` | `all` | Which test file/suite to run |
| `BROWSER` | `chromium`, `firefox`, `webkit` | `chromium` | Browser to run tests in |
| `MODE` | `headed`, `headless` | `headed` | Run with UI visible or headless |
| `INSTALL_DEPS` | `true`, `false` | `true` | Whether to install/update dependencies |

## Pipeline Stages

1. **Checkout** - Clones the repository
2. **Setup Python Environment** - Creates venv, installs pytest, playwright, pytest-playwright, pytest-html
3. **Install Playwright Browsers** - Downloads browser binaries and system dependencies
4. **Run Playwright Tests** - Executes pytest with selected parameters

## Reports Generated

- **HTML Report**: `reports/report_<browser>_<build_number>.html` - Interactive Playwright report
- **JUnit XML**: `reports/results_<browser>_<build_number>.xml` - For Jenkins test results trend
- **Screenshots**: Captured on test failure (saved to `test-results/` and copied to `reports/`)

## Setting Up in Jenkins

1. **Create a new Pipeline job** in Jenkins
2. **Configure SCM** - Point to your Git repository
3. **Script Path** - Set to `Jenkinsfile` (or `Jenkinsfile.windows`)
4. **Required Jenkins Plugins**:
   - Pipeline
   - Git
   - HTML Publisher Plugin
   - JUnit Plugin
   - Email Extension Plugin (for email notifications)

## Email Configuration

Update the email addresses in `Jenkinsfile`:
- `to`: Recipient email
- `from`: Sender email
- `replyTo`: Reply-to email

Configure Jenkins email server in **Manage Jenkins → Configure System → Extended E-mail Notification**.

## Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install --with-deps

# Run tests (headed, chromium)
pytest --headed --browser chromium --html=reports/report.html --self-contained-html

# Run tests (headless, firefox)
pytest --headless --browser firefox --html=reports/report.html --self-contained-html

# Run specific test file
pytest test/recording.py --headed --browser chromium
```

## Adding New Tests

1. Create test files in `test/` directory with naming convention `test_*.py` or `*_test.py`
2. Use pytest-playwright fixtures: `page`, `context`, `browser`
3. Add page objects to `pages/` directory
4. Add utilities to `utils/` directory

## Troubleshooting

- **Browser not found**: Run `playwright install --with-deps` manually
- **Permission errors**: Ensure Jenkins agent has permission to create venv and install browsers
- **Slow tests**: Adjust `SLOW_MO` in `.env` or `--slowmo` in pytest args
- **Headless issues**: Some sites block headless - try `--headed` mode

## CI/CD Tips

- Set `INSTALL_DEPS=false` for faster builds after initial setup
- Use `MODE=headless` for CI runs
- Run `BROWSER=chromium` for fastest execution
- Archive `reports/**` for historical test reports