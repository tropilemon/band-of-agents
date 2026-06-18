"""The ONLY file that directly reads and writes to employee_dataset.csv.
All other files and agents must go through this file to access employee data.
Contains raw, unmasked data operations, so always call from agent1_onboarding.py
after Agent 2 security approval. Never import this directly into any AI agent"""

import pandas as pd
from datetime import date
df = pd.read_csv("employee_dataset.csv")

#Fetches one employee's REAL data from the database by their employee ID
#WARNING: Return real unmasked data, should only be called within data_loader.py
def get_employee(employee_id):
    return df[df["employee_id"] == employee_id].iloc[0].to_dict()

#Fetches one specific field for one employee from the REAL database
#WARNING: Return real unmasked data, should only be called within data_loader.py
def get_field(employee_id, field):
    employee = df[df["employee_id"] == employee_id].iloc[0].to_dict()
    return employee[field]

#Adds a new employee to the real database CSV.
#WARNING: Only call this from agent1_onboarding.py after Agent 2 security approval.
def add_employee(details):
    global df

    #Automatically generates next employee ID
    last_id = df["employee_id"].iloc[-1]
    next_id = int(last_id[1:])+1 #kinda confuse on this line
    auto_id = f"E{next_id:03d}"

    #Smart defaulting some info
    new_employee = {
        "employee_id" : auto_id,
        "name" : details["name"],
        "department" : details["department"],
        "job_title" : details["job_title"],
        "employment_type" : details["employment_type"],
        "base_salary" : details["base_salary"],
        "start_date": details.get("start_date", str(date.today())),
        "health_insurance": details.get("health_insurance", 
                            "Yes" if details["employment_type"] == "Full-Time" else "No"),
        "retirement_contribution": details.get("retirement_contribution", "3%"),
        "stock_options": details.get("stock_options", "No"),
        "region": details["region"]
    }

    new_row = pd.DataFrame([new_employee])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("employee_dataset.csv", index=False)
    
    return f"{new_employee['name']} added as {auto_id}"

#Updates one specific field for one employee in the real database.
#WARNING: Writes real data so only call from agent1 after Agent 2 approval.
def update_employee(employee_id, field, new_value):
    global df
    
    # check if employee exists first
    if not (df["employee_id"] == employee_id).any():
        return f"Employee {employee_id} not found"
    
    # update the specific field
    df.loc[df["employee_id"] == employee_id, field] = new_value
    
    # save back to CSV
    df.to_csv("employee_dataset.csv", index=False)
    
    return f"Updated {field} to {new_value} for {employee_id}"

#Permanently removes an employee from the real database CSV   
def delete_employee(employee_id):
    global df
    
    # check if employee exists first
    if not (df["employee_id"] == employee_id).any():
        return f"Employee {employee_id} not found"
    df = df[df["employee_id"] != employee_id]

    # save back to CSV
    df.to_csv("employee_dataset.csv", index=False)
    
    return f"Deleted {employee_id} from database"

#Returns all employees as a list of dictionaries
#WARNING: Returns real unmasked data, so always anonymize before passing to agents
def get_all_employees():
    return df.to_dict(orient="records")