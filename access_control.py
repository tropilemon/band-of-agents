# agent 1: access control for payroll data
from users import USERS

ROLES = {
    #Mia's
    "admin": ["view_employee", "add_employee", "update_employee", "delete_employee",
        "record_absence", "view_absence", "delete_absence", "update_absence",
        "calc_deduction", "calc_benefits", "view_benefits", "run_payroll"],
    "senior_hr": ["view_employee", "record_absence", "view_absence", "update_absence",
        "calc_deduction", "calc_benefits", "view_benefits", "run_payroll"],
    "manager": ["view_employee", "record_absence", "view_absence", "view_benefits"],
    "junior_hr": ["view_absence", "record_absence"]
}


def authorize(role, action):
    return action in ROLES.get(role, [])