import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from provision_user import provision_user
from provision_user import create_azure_user
from provision_user import create_jira_user

def test_create_azure_user_returns_success():
    result = create_azure_user("John Doe", "john@company.com", "Engineer")
    assert result["status"] == "created"
    assert result["user"] == "john@company.com"

def test_create_jira_user_returns_success():
    result = create_jira_user("John Doe", "john@company.com", "Engineer")
    assert result["status"] == "created"
    assert result["user"] == "john@company.com"

def test_provison_user_success():
    result = provision_user("John Doe", "john@company.com", "Engineer")
    assert result["status"] == "success"
    assert "azure" in result
    assert "jira" in result

def test_provision_user_returns_both_systems():
    result = provision_user("Jane Doe", "jane@company.com", "Admin")
    assert result["azure"]["status"] == "created"
    assert result["jira"]["status"] == "created"