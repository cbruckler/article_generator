from simple_salesforce import Salesforce
import os

# Connect to Salesforce
def connect_to_salesforce(username, password, security_token):
    try:
        sf = Salesforce(username=username, password=password, security_token=security_token)
        print("Connected to Salesforce!")
        return sf
    except Exception as e:
        print(f"Error connecting to Salesforce: {e}")
        return None

# Fetch cases from Salesforce
def fetch_cases(sf, query="SELECT Id, CaseNumber, Subject, Description, Status FROM Case"):
    try:
        cases = sf.query(query)
        return cases.get("records", [])
    except Exception as e:
        print(f"Error fetching cases: {e}")
        return []

# Generate article content
def generate_article(case):
    title = f"Case #{case['CaseNumber']}: {case['Subject']}"
    body = (
        f"**Case Number**: {case['CaseNumber']}\n\n"
        f"**Subject**: {case['Subject']}\n\n"
        f"**Status**: {case['Status']}\n\n"
        f"**Description**:\n{case['Description']}\n\n"
    )
    return title, body

# Save articles to files
def save_article(title, body, directory="articles"):
    # Create directory if not exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Clean title for filename
    filename = os.path.join(directory, f"{title.replace(' ', '_').replace('#', '')}.txt")
    try:
        with open(filename, "w") as file:
            file.write(f"{title}\n\n{body}")
        print(f"Article saved: {filename}")
    except Exception as e:
        print(f"Error saving article: {e}")

# Main function
def main():
    # Replace these with your Salesforce credentials
    username = "your_salesforce_username"
    password = "your_salesforce_password"
    security_token = "your_salesforce_security_token"

    # Connect to Salesforce
    sf = connect_to_salesforce(username, password, security_token)
    if not sf:
        return

    # Fetch cases
    cases = fetch_cases(sf)

    # Generate and save articles
    for case in cases:
        title, body = generate_article(case)
        save_article(title, body)

if __name__ == "__main__":
    main()
