from agent2_security import run_security_check
from agent1_onboarding import ag1_get_employee_field
from absence_loader import record_absence, get_used_paid_days, delete_absence, update_absence, get_all_absences, get_absence_by_month, get_absence_by_employee, get_absence_by_field
from deduction_ai import get_deduction_rules
from datetime import datetime

def ag3_record_absence(user, employee_id, date, abs_type, hrs_missed, region, emp_type):
    if run_security_check(user, "record_absence"):
        record_absence(employee_id, date, abs_type, hrs_missed, region, emp_type)
        return f"Absence for {employee_id} recorded successfully"
    else:
        return "Invalid action"

def ag3_get_used_paid_days(user, employee_id, absence_type):
    if run_security_check(user, "record_absence"):
        return get_used_paid_days(employee_id, absence_type)
    else:
        return "Invalid action"

def ag3_delete_absence(user, emp_id, date, abs_type):
    if run_security_check(user, "record_absence"):
        delete_absence(emp_id, date, abs_type)
    else:
        return "Invalid action"

def ag3_update_absence(user, employee_id, field, new_value):
    if run_security_check(user, "record_absence"):
        update_absence(employee_id, field, new_value)
    else:
        return "Invalid action"
    
def ag3_get_all_absences(user):
    if run_security_check(user, "record_absence"):
        return get_all_absences()
    else:
        return "Invalid action"
    
def ag3_get_absence_by_month(user, month, year):
    if run_security_check(user, "record_absence"):
        return get_absence_by_month(month, year)
    else:
        return "Invalid action"
    
def ag3_get_absence_by_employee(user, employee_id):
    if run_security_check(user, "record_absence"):
        return get_absence_by_employee(employee_id)
    else:
        return "Invalide action"

def get_absence_field(user, employee_id, field):
    if run_security_check(user, "record_absence"):
        return get_absence_by_field(employee_id, field)
    else:
        return "Invalid action"
    
def flag_for_hr_review(employee_id, absence_type):
    return (f"{absence_type} for {employee_id} requires HR review")
    
def ag3_calculate_deduction(user, employee_id, month, year):
    if run_security_check(user, "record_absence"):
        absence_type = get_absence_field(user, employee_id, "absence_type")
        region = ag1_get_employee_field(user, employee_id, "region")
        employment_type = ag1_get_employee_field(user, employee_id, "employment_type")
        if (absence_type != "Access denied") and (region != "Invalid action") and (employment_type != "Invalid action"):
            deduction_result = get_deduction_rules(absence_type, region, employment_type)
        else:
            return "Invalid inputs"

        if deduction_result["requires_hr_review"]:
            return flag_for_hr_review(employee_id, absence_type)
        
        if ag3_get_used_paid_days(user, employee_id, absence_type) <= deduction_result["paid_days_allowed"]:
            return 0
        
        absences = get_absence_by_month(month, year)
        employee_absences = [
            a for a in absences
            if a["employee_id"] == employee_id
            and a["absence_type"] == absence_type
        ]

        base_salary = ag1_get_employee_field(user, employee_id, "base_salary")
        deduction = 0

        if deduction_result["deduction_type"] == "full_day":
            days_missed = len(employee_absences)
            daily_rate = base_salary / 260
            deduction = daily_rate * days_missed
        elif deduction_result["deduction_type"] == "hourly":
            hours_missed = sum(a["hours_missed"] for a in employee_absences)
            hourly_rate = base_salary / 2080
            deduction = hourly_rate * hours_missed
        elif deduction_result["deduction_type"] == "none":
            deduction = 0
    
        return deduction
    return "Invalid action"

def ag3_flag_excessive_absences(user, employee_id, month, year):
    if run_security_check(user, "view_payroll"):
        absences = get_absence_by_employee(employee_id)
        monthly = [
            a for a in absences
            if datetime.strptime(a["date"], "%Y-%m-%d").month == month
        ]
        if len(monthly) >= 3:
            print(f"{employee_id} has {len(monthly)} absences this month")
            return True
        return False
    return "Invalid action"
