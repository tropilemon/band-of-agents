from data_loader import get_all_employees, get_employee, get_field, add_employee, update_employee, delete_employee
from agent2_security import run_security_check
from anonymizer import anonymize_all, anonymize_one, anonymize_name, anonymize_id

def ag1_get_all_employees(user):
    if run_security_check(user, "view_payroll") == True:
        real_data = get_all_employees()
        anon_data = anonymize_all(real_data)
        return anon_data
    else:
        return "Access denied"
    
def ag1_get_one_employee(user, id):
    if run_security_check(user, "view_payroll") == True:
        real_data = get_employee(id)
        anon_data = anonymize_one(real_data)
        return anon_data
    return "Access denied"
    
def ag1_get_employee_field(user, id, field):
    if run_security_check(user, "view_payroll") == True:
        if field == "name":
            real_name = get_field(id, "name")
            anon_name = anonymize_name(real_name)
            return anon_name
        elif field == "employee_id":
            real_id = get_field(id, "employee_id")
            anon_id = anonymize_id(real_id)
            return anon_id
        else:
            return get_field(id, field)
    else:
        return "Access denied"

def ag1_add_employee(user, name, dpt, job_title, emp_type, base_salary, region):
    if run_security_check(user, "add_employee") == True:
        details = {
            "name":name,
            "department":dpt,
            "job_title":job_title,
            "employment_type": emp_type,
            "base_salary":base_salary,
            "region": region
        }
        return(add_employee(details))
    else:
        return "Access denied"

def ag1_add_employee_prompt(user):
    if run_security_check(user, "add_employee") == True:
        name = input("New employee's name: ")
        dpt = input("New employee's department: ")
        job_title = input("New employee's job title: ")
        base_salary = int(input("New employee's base salary: "))
        region = input("New employee's working region: ")
        emp_type_choice = input("Employment type? 1 Full Time, 2 Part Time (type only numbers)")
        if emp_type_choice == "1":
            emp_type = "Full Time"
        elif emp_type_choice == "2":
            emp_type = "Part Time"
        else: 
            print("Invalid input")
            return "Invalid"
        ag1_add_employee(user, name, dpt, job_title, emp_type, base_salary, region)
    else:
        return "Access denied"
        
def ag1_update_employee(user, id, field, update):
    if run_security_check(user, "update_employee") == True:
        return(update_employee(id, field, update))
    else:
        return "Access denied"
        
def ag1_delete_employee(user, id):
    if run_security_check(user, "delete_employee") == True:
        return(delete_employee(id))
    else:
        return "Access denied"

# test calls — remove these when done testing
if __name__ == "__main__":
    print(ag1_add_employee("anna smith", "Andy Chang", "Finance", "Junior Analyst", "Full-Time", 100000))