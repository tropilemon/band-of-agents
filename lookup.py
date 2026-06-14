"""Handles unscrambling anonymized data back to real values.
Only used at the very end of the workflow when returning results to HR.
Never called by AI agents bcs it's only called after AI processing is complete"""

#Builds a dictionary mapping anonymized codes back to real values.
#Only built after AI processing is complete. This is never passed to any AI agent
def build_lookup_table(anonymized_list, original_list):
    lookup = {}
    for i in range(len(anonymized_list)):
        lookup[anonymized_list[i]["employee_id"]] = original_list[i]["employee_id"]
        lookup[anonymized_list[i]["name"]] = original_list[i]["name"]
    return lookup

def unscamble(report, lookup_table):
    pass