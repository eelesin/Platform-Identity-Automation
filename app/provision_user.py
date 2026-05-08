import json


def create_azure_user(name, email, role):
    return {"status": "created", "user": email}

def create_jira_user(name, email, role):
    return {"status": "created", "user": email}

def provision_user(name, email, role):
    try:
        azure_result = create_azure_user(name, email, role)
        jira_result = create_jira_user(name, email, role)
        return {
            "status": "success",
            "azure": azure_result,
            "jira": jira_result
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}
    
if __name__ == "__main__":
        result = provision_user("John Doe", "john@company.com", "Engineer")
        print(json.dumps(result, indent=2))