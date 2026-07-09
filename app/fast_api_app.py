"""
AttriSense AI — FastAPI Application
Custom HR Dashboard + REST API endpoints
LTTS Global Hackathon 2026
"""

import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from app.mcp_server import EMPLOYEES, _calculate_score, _get_level, _get_prediction_window

app = FastAPI(
    title="AttriSense AI",
    description="Predictive Employee Attrition Intelligence Platform — LTTS Global Hackathon 2026",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATION SYSTEM STATE
# ─────────────────────────────────────────────────────────────────────────────
NOTIFICATIONS = [
    {
        "id": 1,
        "type": "ALARM",
        "sender": "System Monitor",
        "recipient": "Analyst",
        "employee_id": "EMP0375",
        "employee_name": "Ashish Wagh",
        "message": "Employee EMP0375 risk score reached 86.1% (CRITICAL threshold breached).",
        "timestamp": "2026-07-09T10:15:30Z",
        "status": "UNREAD",
        "notes": ""
    },
    {
        "id": 2,
        "type": "ALARM",
        "sender": "System Monitor",
        "recipient": "Analyst",
        "employee_id": "EMP0783",
        "employee_name": "Bhavesh Fernandez",
        "message": "Employee EMP0783 risk score reached 86.0% (CRITICAL threshold breached).",
        "timestamp": "2026-07-09T11:04:12Z",
        "status": "READ",
        "notes": "Forwarded to HR with review notes."
    },
    {
        "id": 3,
        "type": "FORWARD",
        "sender": "Analyst (Risk Control)",
        "recipient": "HR Team",
        "employee_id": "EMP0783",
        "employee_name": "Bhavesh Fernandez",
        "message": "Risk alert forwarded for review. Compensation is below 30th percentile despite high performance.",
        "timestamp": "2026-07-09T11:05:00Z",
        "status": "UNREAD",
        "notes": "Waiting for HR discussion with Manager."
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# REST API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/risk-overview")
def risk_overview():
    """Returns all employee risk scores sorted by risk descending."""
    results = []
    for eid, emp in EMPLOYEES.items():
        result = _calculate_score(emp)
        score = result["total"]
        level = _get_level(score)
        top_driver = max(result["breakdown"].items(), key=lambda x: x[1])[0]
        results.append({
            "employee_id": eid,
            "name": emp["name"],
            "department": emp["department"],
            "manager": emp.get("manager", "Unknown Manager"),
            "tenure_years": emp["tenure_years"],
            "score": score,
            "level": level,
            "top_driver": top_driver.replace("_", " ").title(),
            "mood": emp["mood_index"],
            "sentiment": emp["sentiment_score"],
            "feedback": emp["feedback"],
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return JSONResponse(content=results)


@app.get("/api/department-heatmap")
def department_heatmap():
    """Returns department-level aggregate risk data."""
    departments = list({emp["department"] for emp in EMPLOYEES.values()})
    dept_data = []
    color_map = {"CRITICAL": "#ef4444", "HIGH": "#f97316", "MODERATE": "#eab308", "LOW": "#22c55e"}

    for dept in sorted(departments):
        dept_employees = {eid: emp for eid, emp in EMPLOYEES.items() if emp["department"] == dept}
        scores = []
        dist = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
        for eid, emp in dept_employees.items():
            r = _calculate_score(emp)
            s = r["total"]
            lv = _get_level(s)
            scores.append(s)
            dist[lv] += 1

        avg = round(sum(scores) / len(scores), 1) if scores else 0
        avg_level = _get_level(avg)
        dept_data.append({
            "department": dept,
            "employee_count": len(dept_employees),
            "avg_risk_score": avg,
            "avg_risk_level": avg_level,
            "distribution": dist,
            "color": color_map.get(avg_level, "#6b7280"),
        })
    return JSONResponse(content=dept_data)


@app.get("/api/employee/{employee_id}")
def get_employee(employee_id: str):
    """Returns full analysis data for a specific employee."""
    eid = employee_id.strip().upper()
    if eid not in EMPLOYEES:
        return JSONResponse(status_code=404, content={"error": f"Employee {eid} not found."})
    emp = EMPLOYEES[eid].copy()
    result = _calculate_score(emp)
    score = result["total"]
    level = _get_level(score)
    emp["employee_id"] = eid
    emp["risk_score"] = score
    emp["risk_level"] = level
    emp["prediction_window"] = _get_prediction_window(level)
    emp["breakdown"] = result["breakdown"]
    top_drivers = sorted(result["breakdown"].items(), key=lambda x: x[1], reverse=True)[:5]
    emp["top_drivers"] = [{"parameter": k, "contribution": v} for k, v in top_drivers]
    return JSONResponse(content=emp)


@app.put("/api/employee/{employee_id}")
async def edit_employee(employee_id: str, request: Request):
    """
    Edits an existing employee's data.
    Restricts field changes based on the user's role.
    """
    eid = employee_id.strip().upper()
    if eid not in EMPLOYEES:
        return JSONResponse(status_code=404, content={"error": f"Employee {eid} not found."})

    try:
        body = await request.json()
        role = str(body.get("role", "HR_ADMIN")).strip()
        data = body.get("data", {})
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON body."})

    emp = EMPLOYEES[eid]

    # Fields that can be edited by HR_ADMIN:
    hr_fields = ["name", "department", "tenure_years", "salary_percentile", "years_since_promotion", "manager"]
    # Fields that can be edited by ANALYST:
    analyst_fields = ["absenteeism_rate", "meeting_participation", "collaboration_index", "sentiment_score", "feedback", "mood_index"]
    # Fields that can be edited by MANAGER:
    manager_fields = ["manager_scorecard", "feedback", "mood_index"]
    # Fields that can be edited by both HR and Analyst:
    common_fields = ["training_count_ytd", "certifications", "awards_count", "internal_job_searches", "cross_functional_work", "team_outings_attended", "weekly_hours"]

    allowed_updates = []
    if role == "HR_ADMIN":
        allowed_updates = hr_fields + common_fields
    elif role == "ANALYST":
        allowed_updates = analyst_fields + common_fields
    elif role == "MANAGER":
        allowed_updates = manager_fields
    else:
        return JSONResponse(status_code=403, content={"error": f"Role {role} not authorized to edit employee data."})

    updated_fields = []
    for k, v in data.items():
        if k in allowed_updates and k in emp:
            if isinstance(emp[k], bool):
                emp[k] = bool(v)
            elif isinstance(emp[k], int):
                emp[k] = int(v)
            elif isinstance(emp[k], float):
                emp[k] = float(v)
            else:
                emp[k] = str(v).strip()
            updated_fields.append(k)

    result = _calculate_score(emp)
    
    new_id = max([n["id"] for n in NOTIFICATIONS], default=0) + 1
    NOTIFICATIONS.append({
        "id": new_id,
        "type": "INFO",
        "sender": "System Logger",
        "recipient": "HR Team" if role != "HR_ADMIN" else "Analyst",
        "employee_id": eid,
        "employee_name": emp["name"],
        "message": f"Employee {eid} data updated by {role}. Fields: {', '.join(updated_fields)}.",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "UNREAD",
        "notes": f"New risk score: {result['total']}% ({_get_level(result['total'])})"
    })

    return JSONResponse(content={
        "status": "success", 
        "employee_id": eid, 
        "updated_fields": updated_fields,
        "new_score": result["total"],
        "new_level": _get_level(result["total"])
    })


@app.post("/api/employee/{employee_id}/action")
async def employee_action(employee_id: str, request: Request):
    """Handles employee self-service actions (wellness support, team transfer, pay reviews)"""
    eid = employee_id.strip().upper()
    if eid not in EMPLOYEES:
        return JSONResponse(status_code=404, content={"error": f"Employee {eid} not found."})

    try:
        body = await request.json()
        action_type = str(body.get("action_type", "")).strip()
        notes = str(body.get("notes", "")).strip()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON body."})

    emp = EMPLOYEES[eid]
    recipient = "Manager"
    message = ""

    if action_type == "HIKE_REQUEST":
        recipient = emp.get("manager", "Tarun Gupta")
        message = f"Salary hike benchmark review requested by employee {emp['name']} ({eid}). Notes: {notes or 'Requesting market benchmark adjustment.'}"
        emp["feedback"] = f"[Employee Action: Hike Request - {notes}] {emp['feedback']}"
        emp["internal_job_searches"] = min(emp["internal_job_searches"] + 2, 15)
    elif action_type == "TRANSFER_REQUEST":
        recipient = "HR Team"
        message = f"Internal team transfer request submitted by employee {emp['name']} ({eid}) due to team alignment concerns. Notes: {notes or 'Requesting internal team shift.'}"
        emp["feedback"] = f"[Employee Action: Transfer Request - {notes}] {emp['feedback']}"
        emp["internal_job_searches"] = min(emp["internal_job_searches"] + 4, 15)
    elif action_type == "WELLNESS_REQUEST":
        recipient = "HR Team"
        message = f"Confidential wellness support check-in requested by employee {emp['name']} ({eid})."
        emp["feedback"] = f"[Employee Action: Wellness Support Request] {emp['feedback']}"
    elif action_type == "ACK_FEEDBACK":
        recipient = emp.get("manager", "Tarun Gupta")
        message = f"Employee {emp['name']} ({eid}) acknowledged performance & absenteeism feedback. Notes: {notes or 'Acknowledged.'}"
        emp["feedback"] = f"[Employee Action: Acknowledged Feedback - {notes}] {emp['feedback']}"
        emp["absenteeism_rate"] = max(emp["absenteeism_rate"] - 0.04, 0.0)
    else:
        return JSONResponse(status_code=400, content={"error": f"Unknown action type: {action_type}"})

    new_id = max([n["id"] for n in NOTIFICATIONS], default=0) + 1
    NOTIFICATIONS.append({
        "id": new_id,
        "type": "FORWARD" if action_type == "HIKE_REQUEST" else "ALARM",
        "sender": f"Employee {emp['name']}",
        "recipient": recipient,
        "employee_id": eid,
        "employee_name": emp["name"],
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "UNREAD",
        "notes": notes
    })

    return JSONResponse(content={"status": "success", "message": "Action logged and manager/HR notified successfully."})


@app.get("/api/notifications")
def get_notifications():
    """Returns cross-departmental notifications, sorted by timestamp descending."""
    return JSONResponse(content=sorted(NOTIFICATIONS, key=lambda x: x["timestamp"], reverse=True))


@app.post("/api/notifications")
async def create_notification(request: Request):
    """Creates a new notification representing cross-departmental actions."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON body."})

    new_id = max([n["id"] for n in NOTIFICATIONS], default=0) + 1
    new_notif = {
        "id": new_id,
        "type":          str(body.get("type", "INFO")).strip().upper(),
        "sender":        str(body.get("sender", "System")).strip(),
        "recipient":     str(body.get("recipient", "HR Team")).strip(),
        "employee_id":   str(body.get("employee_id", "")).strip().upper(),
        "employee_name": str(body.get("employee_name", "")).strip(),
        "message":       str(body.get("message", "")).strip(),
        "timestamp":     datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status":        "UNREAD",
        "notes":         str(body.get("notes", "")).strip()
    }
    NOTIFICATIONS.append(new_notif)

    eid = new_notif["employee_id"]
    if eid and eid in EMPLOYEES:
        if new_notif["type"] == "MANAGER_ACTION":
            prev = EMPLOYEES[eid].get("feedback", "")
            EMPLOYEES[eid]["feedback"] = f"Manager Action Taken ({new_notif['sender']}): {new_notif['message']}. Details: {new_notif['notes']}. Previous: {prev}"
        elif new_notif["type"] == "FORWARD" and new_notif["notes"]:
            for n in NOTIFICATIONS:
                if n["employee_id"] == eid and n["type"] == "ALARM":
                    n["status"] = "READ"

    return JSONResponse(status_code=201, content=new_notif)


@app.get("/api/manager-analytics")
def get_manager_analytics():
    """Aggregates employee risk data by manager to identify toxic hotspots."""
    mgr_stats = {}
    for emp in EMPLOYEES.values():
        mgr = emp.get("manager", "Unknown Manager")
        dept = emp.get("department", "Engineering")
        if mgr not in mgr_stats:
            mgr_stats[mgr] = {
                "manager": mgr,
                "department": dept,
                "team_size": 0,
                "scores": [],
                "critical_count": 0,
                "high_count": 0,
                "moderate_count": 0,
                "low_count": 0
            }
        
        r = _calculate_score(emp)
        s = r["total"]
        lv = _get_level(s)
        
        mgr_stats[mgr]["team_size"] += 1
        mgr_stats[mgr]["scores"].append(s)
        mgr_stats[mgr][f"{lv.lower()}_count"] += 1

    results = []
    for mgr, d in mgr_stats.items():
        avg = round(sum(d["scores"]) / len(d["scores"]), 1) if d["scores"] else 0.0
        risk_ratio = (d["critical_count"] + d["high_count"]) / d["team_size"] if d["team_size"] > 0 else 0.0
        
        if risk_ratio >= 0.25 or d["critical_count"] >= 3:
            status = "🔴 HIGH ATTRITION LEAK"
        elif risk_ratio >= 0.12 or d["high_count"] >= 2:
            status = "🟠 WATCH LIST"
        else:
            status = "🟢 STABLE TEAM"

        results.append({
            "manager": d["manager"],
            "department": d["department"],
            "team_size": d["team_size"],
            "avg_risk_score": avg,
            "critical_count": d["critical_count"],
            "high_count": d["high_count"],
            "moderate_count": d["moderate_count"],
            "low_count": d["low_count"],
            "manager_status": status
        })

    results.sort(key=lambda x: (x["manager_status"].startswith("🔴"), x["critical_count"] + x["high_count"], x["avg_risk_score"]), reverse=True)
    return JSONResponse(content=results)


def generate_simulated_report(emp_id: str, emp: dict) -> str:
    """Generates a beautiful multi-agent mock report if Gemini daily API limits are hit."""
    from app.mcp_server import DRIVER_ACTIONS

    result = _calculate_score(emp)
    score = result["total"]
    level = _get_level(score)
    window = _get_prediction_window(level)
    breakdown = result["breakdown"]

    top_drivers = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:5]
    primary_driver = top_drivers[0][0]

    sent = emp.get("sentiment_score", 0.0)
    mood = "Engaged" if sent >= 0.2 else "Neutral" if sent >= -0.2 else "Disengaged"
    themes = []
    if sent < -0.2:
        if emp.get("salary_percentile", 50) < 40:
            themes.append("compensation_concern")
        if emp.get("years_since_promotion", 0) > 3.0:
            themes.append("career_stagnation")
        if emp.get("absenteeism_rate", 0) > 0.15:
            themes.append("burnout")
        if emp.get("manager_scorecard", 10) < 5.0:
            themes.append("manager_conflict")
    if not themes:
        themes = ["general_engagement"]

    theme_str = ", ".join(themes)

    actions = DRIVER_ACTIONS.get(primary_driver, [
        "Review career progression path with employee.",
        "Set up a 1-on-1 check-in to discuss goals.",
        "Provide direct recognition for recent contributions."
    ])

    report = f"""═══════════════════════════════════════════════════════
ATTRISENSE AI — EMPLOYEE ATTRITION RISK INTELLIGENCE
LTTS Global Hackathon 2026 [SIMULATION FALLBACK ACTIVE]
═══════════════════════════════════════════════════════
EMPLOYEE: {emp["name"]} | {emp["department"]} | {emp["tenure_years"]} years tenure
ANALYSIS DATE: {datetime.now(timezone.utc).strftime("%d-%m-%Y")}

📊 ATTRITION RISK SCORE: {score}% — {level}
⏰ PREDICTION WINDOW: {window}

🔴 TOP RISK DRIVERS:
"""
    for i, (k, v) in enumerate(top_drivers, 1):
        report += f"{i}. {k.replace('_', ' ').title()}: contributed {v} points to risk score\n"

    report += f"""
😔 SENTIMENT ANALYSIS:
Mood: {mood} | Score: {sent}
Themes: {theme_str}
Employee is displaying indicators of {themes[0].replace('_', ' ')} based on feedback NLP: "{emp.get("feedback", "")}"

📡 SIGNAL DASHBOARD:
"""
    for k, v in breakdown.items():
        light = "🔴" if v > (12 * 0.7 if k == "absenteeism" else 10 * 0.7) else "🟠" if v > (12 * 0.4 if k == "absenteeism" else 10 * 0.4) else "🟢"
        report += f"- {k.replace('_', ' ').title()}: {light} ({v} pts contribution)\n"

    report += f"""
💡 RETENTION PLAN:
1. Priority Action: {actions[0]} | Owner: HR_ADMIN | Timeline: Within 2 weeks
2. Supporting Action: {actions[1]} | Owner: MANAGER | Timeline: Within 30 days
3. Operational Action: {actions[2] if len(actions)>2 else "Monitor engagement weekly"} | Owner: TEAM_LEAD | Timeline: Within 60 days

🎯 KEY INSIGHT:
High flight risk is primarily driven by {primary_driver.replace('_', ' ')} compounded by pulse sentiment.

⚠️ HR ACTION REQUIRED: {"YES — escalate immediately" if level in ["CRITICAL", "HIGH"] else "MONITOR — schedule quarterly review"}
═══════════════════════════════════════════════════════"""
    return report


@app.post("/api/employee/{employee_id}/analyze")
async def analyze_employee_agent(employee_id: str, request: Request):
    """
    Invokes the Google ADK 2.4.0 Orchestrator programmatically.
    If the daily Gemini free-tier request limit is exceeded,
    automatically returns a high-fidelity simulated fallback.
    """
    import asyncio
    eid = employee_id.strip().upper()
    if eid not in EMPLOYEES:
        return JSONResponse(status_code=404, content={"error": f"Employee {eid} not found."})

    try:
        body = await request.json()
        role = str(body.get("role", "HR_ADMIN")).strip()
    except Exception:
        role = "HR_ADMIN"

    from google.adk.agents.run_config import RunConfig, StreamingMode
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types
    from app.agent import root_agent

    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="dashboard_user", app_name="attrisense")
    session.state["requester_role"] = role
    
    runner = Runner(agent=root_agent, session_service=session_service, app_name="attrisense")
    message = types.Content(
        role="user", parts=[types.Part.from_text(text=f"analyze {eid}")]
    )

    def run_adk():
        return list(
            runner.run(
                new_message=message,
                user_id="dashboard_user",
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.NONE),
            )
        )

    try:
        events = await asyncio.to_thread(run_adk)
        final_text = ""
        for event in events:
            if hasattr(event, "content") and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        final_text += part.text
        
        if not final_text:
            final_text = generate_simulated_report(eid, EMPLOYEES[eid])
    except Exception as e:
        final_text = generate_simulated_report(eid, EMPLOYEES[eid])

    return JSONResponse(content={"report": final_text})


@app.post("/api/employee")
async def add_employee(request: Request):
    """Add a new employee via user entry."""
    import app.mcp_server as mcp_mod

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON body."})

    required = ["name", "department", "tenure_years", "performance_trend",
                "absenteeism_rate", "meeting_participation", "collaboration_index",
                "manager_scorecard", "years_since_promotion", "training_count_ytd",
                "certifications", "awards_count", "internal_job_searches",
                "cross_functional_work", "team_outings_attended",
                "salary_percentile", "sentiment_score", "feedback", "mood_index"]
    missing = [f for f in required if f not in body]
    if missing:
        return JSONResponse(status_code=400, content={"error": f"Missing fields: {missing}"})

    existing_ids = [int(eid.replace("EMP", "")) for eid in mcp_mod.EMPLOYEES if eid.startswith("EMP") and eid[3:].isdigit()]
    next_num = max(existing_ids, default=0) + 1
    new_id = f"EMP{next_num:04d}"

    tenure = float(body["tenure_years"])

    new_emp = {
        "name":                  str(body["name"]).strip(),
        "department":            str(body["department"]).strip(),
        "tenure_years":          tenure,
        "is_fresher":            tenure < 1.5,
        "base_location_match":   bool(body.get("base_location_match", True)),
        "salary_percentile":     int(body["salary_percentile"]),
        "performance_trend":     str(body["performance_trend"]),
        "absenteeism_rate":      float(body["absenteeism_rate"]),
        "meeting_participation": float(body["meeting_participation"]),
        "collaboration_index":   float(body["collaboration_index"]),
        "manager_scorecard":     float(body["manager_scorecard"]),
        "years_since_promotion": float(body["years_since_promotion"]),
        "training_count_ytd":    int(body["training_count_ytd"]),
        "certifications":        int(body["certifications"]),
        "awards_count":          int(body["awards_count"]),
        "internal_job_searches": int(body["internal_job_searches"]),
        "cross_functional_work": bool(body["cross_functional_work"]),
        "team_outings_attended": int(body.get("team_outings_attended", 0)),
        "sentiment_score":       float(body.get("sentiment_score", 0.0)),
        "feedback":              str(body["feedback"]),
        "mood_index":            float(body["mood_index"]),
        "weekly_hours":          float(body.get("weekly_hours", 40.0)),
    }

    # Assign Manager based on department rules
    dept = new_emp["department"]
    if dept == "Engineering":
        r_calc = _calculate_score(new_emp)
        if r_calc["total"] >= 60:
            new_emp["manager"] = "Tarun Gupta"
        else:
            new_emp["manager"] = "Suresh Patil" if r_calc["total"] < 35 else "Rakesh Sharma"
    elif dept == "Product":
        new_emp["manager"] = "Sneha Roy"
    elif dept == "Sales":
        new_emp["manager"] = "Rajesh Kumar"
    elif dept == "Finance":
        new_emp["manager"] = "Anjali Menon"
    elif dept == "HR":
        new_emp["manager"] = "Kavita Nair"
    elif dept == "Operations":
        new_emp["manager"] = "Amit Verma" if float(body["manager_scorecard"]) < 6.0 else "Deepak Joshi"
    elif dept == "Marketing":
        new_emp["manager"] = "Sanjay Patel"
    elif dept == "Data Science":
        new_emp["manager"] = "Aditya Sen"
    elif dept == "IT":
        new_emp["manager"] = "Neha Sharma"
    else:
        new_emp["manager"] = "Zara Khan"

    mcp_mod.EMPLOYEES[new_id] = new_emp

    result  = _calculate_score(new_emp)
    score   = result["total"]
    level   = _get_level(score)
    window  = _get_prediction_window(level)
    top_drivers = sorted(result["breakdown"].items(), key=lambda x: x[1], reverse=True)[:5]

    return JSONResponse(status_code=201, content={
        "employee_id":       new_id,
        "name":              new_emp["name"],
        "department":        new_emp["department"],
        "risk_score":        score,
        "risk_level":        level,
        "prediction_window": window,
        "top_drivers":       [{"parameter": k, "contribution": v} for k, v in top_drivers],
        "message":           f"Employee {new_id} added successfully. Risk level: {level} ({score}%)"
    })


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM HR DASHBOARD LOADER
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """Serves the AttriSense AI custom HR dashboard from dynamic file."""
    html_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Dashboard template error</h1><p>{str(e)}</p>", status_code=500)


@app.get("/", response_class=HTMLResponse)
def root():
    """Redirects root to dashboard."""
    return HTMLResponse(content='<meta http-equiv="refresh" content="0;url=/dashboard">', status_code=302)
