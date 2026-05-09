import json
import csv
import os
import requests
from azure.identity import ClientSecretCredential


def get_graph_token():
     tenant_id = os.environ.get("GRAPH_TENANT_ID")
     client_id = os.environ.get("GRAHP_CLIENT_ID")
     client_secret = os.environ.get("GRAPH_CLIENT_SECRET")

     credential = ClientSecretCredential(
          tenant_id=tenant_id,
          client_id=client_id,
          client_secret=client_secret
     )
     token = credential.get_token("https://graph.microsoft.com/.default")
     return token

def create_azure_user(name, email, role):
     try:
          token = get_graph_token()
          headers = {
               "Authorization": f"Bearer {token}",
               "Content-Type": "application/json"
          }
          #generate temp password
          payload = {
               "accountEnabled": True,
               "displayName": name,
               "mailNickname": email.split("@")[0],
               "userPrincipalName": email,
               "passwordProfile": {
                    "forceChangePasswordNextSignIn": True,
                    "password": "TempPassword@2026!"
               }
          }
          response = requests.post(
               "https://graph.microsoft.com/v1.0/users",
               headers=headers,
               json=payload
          )
          if response.status_code == 201:
               return{"status": "created", "user": email}
          
     except Exception as e:
        return {"status": "failed", "user": email, "error": str(e)}
     
def create_jira_user(name, email, role):
     try:
        jira_url   = os.environ.get("JIRA_URL")
        jira_email = os.environ.get("JIRA_EMAIL")
        jira_token = os.environ.get("JIRA_API_TOKEN")

        response = requests.post(
            f"{jira_url}/rest/api/3/user",
            auth=(jira_email, jira_token),
            headers={"Content-Type": "application/json"},
            json={
                "emailAddress": email,
                "displayName": name,
                "products": []
            }
        )
        if response.status_code == 201:
            return {"status": "created", "user": email}
        else:
            return {
                "status": "failed",
                "user": email,
                "error": response.json()
            }
     except Exception as e:
        return {"status": "failed", "user": email, "error": str(e)}
    

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
        main()