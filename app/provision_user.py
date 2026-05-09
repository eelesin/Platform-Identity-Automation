import json
import csv
import os

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


def new_hires(filename):
     employees = []
      # get absolute path relative to this file
     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
     filepath = os.path.join(base_dir, "data", filename)
     with open(filepath, encoding="utf-8") as file:
          reader = csv.DictReader(file)
          for row in reader:
               employees.append(row)
     return employees

def main():
     new_hires_file = new_hires("new_hires.csv")
     print(f"Processing {len(new_hires_file)} new hires...\n")

     for hire in new_hires_file:
          result = provision_user(
               hire["name"],
               hire["email"],
               hire["role"]
          )
        
    
               
         

if __name__ == "__main__":
        result = provision_user("John Doe", "john@company.com", "Engineer")
        print(json.dumps(result, indent=2))