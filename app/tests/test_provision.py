import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from provision_user import (
    provision_user,
    create_azure_user,
    create_jira_user,
    new_hires
)

# mock Azure Graph API call
@patch("provision_user.requests.post")
@patch("provision_user.get_graph_token")
def test_create_azure_user_success(mock_token, mock_post):
    mock_token.return_value = "fake-token"
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    result = create_azure_user("John Doe", "john@company.com", "Engineer")
    assert result["status"] == "created"
    assert result["user"] == "john@company.com"

# mock Jira API call
@patch("provision_user.requests.post")
def test_create_jira_user_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    result = create_jira_user("John Doe", "john@company.com", "Engineer")
    assert result["status"] == "created"
    assert result["user"] == "john@company.com"

@patch("provision_user.requests.post")
@patch("provision_user.get_graph_token")
def test_provision_user_success(mock_token, mock_post):
    mock_token.return_value = "fake-token"
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    result = provision_user("John Doe", "john@company.com", "Engineer")
    assert result["status"] == "success"
    assert "azure" in result
    assert "jira" in result

def test_read_new_hires_returns_list():
    result = new_hires("new_hires.csv")
    assert isinstance(result, list)

def test_read_new_hires_not_empty():
    result = new_hires("new_hires.csv")
    assert len(result) > 0

def test_read_new_hires_has_correct_keys():
    result = new_hires("new_hires.csv")
    assert "name" in result[0]
    assert "email" in result[0]
    assert "role" in result[0]