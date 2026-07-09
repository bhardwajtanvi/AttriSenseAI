from app.mcp_server import EMPLOYEES, _calculate_score, _get_level

print(f"Total employees: {len(EMPLOYEES)}")

tiers = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
for e in EMPLOYEES.values():
    s = _calculate_score(e)["total"]
    tiers[_get_level(s)] += 1
print("Risk distribution:", tiers)

depts = {}
for e in EMPLOYEES.values():
    depts[e["department"]] = depts.get(e["department"], 0) + 1
print("Departments:", dict(sorted(depts.items())))

first_id, first_emp = list(EMPLOYEES.items())[0]
print(f"Sample: {first_id} -> {first_emp['name']} ({first_emp['department']}) tenure={first_emp['tenure_years']}")
last_id, last_emp = list(EMPLOYEES.items())[-1]
print(f"Last:   {last_id} -> {last_emp['name']} ({last_emp['department']}) tenure={last_emp['tenure_years']}")
