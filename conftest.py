import pytest
from playwright.sync_api import sync_playwright

# Configure pytest-playwright to use our custom browser launch options if needed
# pytest-playwright provides built-in fixtures: browser, context, page, etc.
# These are automatically available when pytest-playwright is installed

# Optional: Custom browser launch configuration
# @pytest.fixture(scope="session")
# def browser_type_launch_args():
#     return {
#         "headless": False,
#         "slow_mo": 200,
#     }

# Optional: Custom context configuration
# @pytest.fixture(scope="function")
# def context(context):
#     # Add custom context setup here if needed
#     yield context