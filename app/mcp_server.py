import json
import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("attrisense-mcp")

# ─────────────────────────────────────────────────────────────────────────────
# 1000-EMPLOYEE DATASET GENERATOR (deterministic seed for reproducibility)
# ─────────────────────────────────────────────────────────────────────────────

_FIRST_NAMES = [
    "Aarav","Aditya","Akash","Amit","Amrita","Ananya","Anjali","Ankit","Ananya","Arjun",
    "Aryan","Ashish","Bhavesh","Chaitali","Chetan","Deepa","Deepak","Divya","Gaurav","Geeta",
    "Harish","Harsha","Hemant","Ishaan","Ishita","Jatin","Jyoti","Kabir","Karan","Kavita",
    "Kirti","Komal","Krishna","Kunal","Lalit","Lata","Mahesh","Manish","Manisha","Meera",
    "Mihir","Mohan","Mohit","Nalini","Neha","Nikhil","Nilesh","Nisha","Nitin","Pallavi",
    "Pankaj","Payal","Pooja","Pradeep","Prakash","Preethi","Priya","Rahul","Raj","Rajan",
    "Rajesh","Rakesh","Ramesh","Ravi","Rekha","Ritesh","Rohit","Roopa","Sachin","Samir",
    "Sandeep","Sangeeta","Sanjay","Sapna","Sarika","Seema","Shilpa","Shiv","Shreya","Shubham",
    "Sneha","Sonam","Sriram","Subhash","Sudhir","Sunil","Sunita","Suresh","Swati","Tanvi",
    "Tarun","Uday","Uma","Varun","Vikas","Vikram","Vinay","Vinita","Vivek","Yogesh",
    "Zara","Aisha","Farhan","Imran","Kavya","Lakshmi","Madhuri","Nandita","Preeti","Saroj",
    "Abhishek","Akanksha","Arpita","Bharat","Deepika","Harsh","Jaya","Kalpana","Monika","Naresh",
    "Nilima","Omkar","Poonam","Pranav","Raghu","Rajeev","Ramya","Rashmi","Ravindra","Ritu",
    "Sameer","Savita","Shyam","Siddharth","Smita","Srikanth","Supriya","Tanya","Tushar","Usha",
    "Vandana","Vijay","Vijaya","Vimal","Vishwas","Yamini","Yash","Yashika","Ashwini","Bhavana",
]

_LAST_NAMES = [
    "Agarwal","Bhatia","Chakraborty","Chaudhary","Choudhury","Das","Desai","Deshpande","Dubey",
    "Gandhi","Ghosh","Goel","Goswami","Gupta","Iyer","Jain","Jha","Joshi","Kapoor","Kapur",
    "Kaur","Khan","Khanna","Kumar","Lal","Mehta","Mishra","Nair","Nambiar","Narayanan",
    "Pande","Pandey","Patel","Patil","Pillai","Prasad","Rao","Reddy","Saxena","Shah",
    "Sharma","Shukla","Singh","Sinha","Srivastava","Subramanian","Tiwari","Tripathi","Varma","Verma",
    "Ahuja","Anand","Arora","Bajaj","Bajpai","Balaji","Banerjee","Basu","Bhatt","Bhattacharya",
    "Chandra","Chatterjee","Dey","Dixit","Fernandez","George","Giri","Hegde","Kamble","Kamath",
    "Krishnan","Laxman","Malhotra","Mathur","Menon","Mohan","Mohanty","Murthy","Naik","Nath",
    "Parikh","Pawar","Rajan","Ramachandran","Rege","Roy","Salunkhe","Sawant","Sen","Sengupta",
    "Sethi","Shinde","Soni","Srinivasulu","Subramaniam","Thakur","Vaidya","Wagh","Yadav","Zade",
]

_DEPARTMENTS = [
    "Engineering", "Engineering", "Engineering",   # weighted higher count
    "Product",
    "Sales",
    "Finance",
    "HR",
    "Operations", "Operations",
    "Marketing",
    "Data Science",
    "IT",
    "Legal",
    "Customer Success",
]

_FEEDBACK_TEMPLATES = {
    "CRITICAL": [
        "Completely burned out. {tenure} years and nothing has changed. Management does not care about growth. Actively searching.",
        "I have been ignored for promotions despite consistently delivering results. Looking at exit options seriously.",
        "The manager relationship is toxic. I feel invisible to leadership. There is no future for me here.",
        "Compensation has not kept up with my contributions. I have better offers on the table now.",
        "Six years and still at the same level. No recognition, no challenge. I am done waiting.",
        "Completely disengaged. No clarity on career path, no support from management. Time to move on.",
        "The internal politics are exhausting. My efforts go unnoticed and I feel undervalued every day.",
        "I cannot sustain this work-life imbalance anymore. Serious burnout, zero recognition, no change in sight.",
        "Feel completely disconnected from the organization. My feedback is never acted upon. Leaving soon.",
        "Had a great start but things have deteriorated rapidly. No growth, hostile manager, considering resignation.",
    ],
    "HIGH": [
        "Starting to feel stuck. The promotion cycle seems unfair and my compensation lags peers.",
        "Miss my hometown and struggling with relocation. Team is okay but it is getting harder.",
        "I give my best every day but my salary has not reflected that. Exploring other opportunities.",
        "Manager gives very little feedback or recognition. Feel like I am not seen.",
        "Not unhappy but not growing either. Starting to wonder if I should look at other companies.",
        "Work-life balance has been poor recently. Feeling early signs of burnout.",
        "Noticed I have been passed over for key projects. Starting to question my fit here.",
        "Team dynamics have become difficult. Not feeling supported in my current role.",
        "Workload has increased significantly without any recognition or compensation adjustment.",
        "Career development conversations never lead anywhere concrete. Getting frustrated.",
    ],
    "MODERATE": [
        "Things are okay here. Would appreciate clearer career path and more challenging work.",
        "Work is decent but could use more learning opportunities. Not fully satisfied.",
        "Neutral about my current role. Could go either way depending on what comes next.",
        "Happy enough with my role but open to better opportunities if they arise.",
        "Work environment is fine. Not overly excited but not looking to leave either.",
        "Somewhat satisfied but wish there was more visible growth trajectory.",
        "Team is good but I would like more recognition for my contributions.",
        "Good work-life balance but could use more growth opportunities. Watching the market.",
        "Settled in but feeling a plateau in terms of skill development.",
        "My manager is supportive but the organization lacks clarity on promotions.",
    ],
    "LOW": [
        "Extremely happy with my role and the team culture. Excited about upcoming projects.",
        "Fantastic learning environment. My manager is a great coach and the team is very collaborative.",
        "Loving the growth trajectory here. Clear career path and excellent recognition.",
        "Best team I have ever worked with. Highly motivated and engaged.",
        "Very satisfied with my compensation, growth, and work-life balance. Plan to stay long term.",
        "Inspired by the vision and direction of this organization. Proud to be part of this team.",
        "Excellent manager who advocates for the team. Great projects and strong recognition culture.",
        "Feel truly valued here. My ideas are heard and my contributions are recognised regularly.",
        "Thriving in my current role. The culture, growth, and compensation all align with my goals.",
        "Could not be happier. Exciting work, great colleagues, supportive leadership, and competitive pay.",
    ],
}

_PERFORMANCE_BY_TIER = {
    "CRITICAL": ["declining", "low_performer", "declining", "low_performer"],
    "HIGH":     ["declining", "stable", "low_performer", "declining"],
    "MODERATE": ["stable", "stable", "improving", "declining"],
    "LOW":      ["high_performer", "improving", "stable", "high_performer"],
}


def _generate_employees() -> dict:
    """Generates 1000 fictitious employees with realistic risk distributions."""
    rng = random.Random(42)  # deterministic seed

    # Risk tier distribution: CRITICAL ~5%, HIGH ~15%, MODERATE ~35%, LOW ~45%
    tiers = (
        ["CRITICAL"] * 50 +
        ["HIGH"]     * 150 +
        ["MODERATE"] * 350 +
        ["LOW"]      * 450
    )
    rng.shuffle(tiers)

    employees = {}

    for i in range(1, 1001):
        emp_id = f"EMP{i:04d}"
        tier = tiers[i - 1]

        first = rng.choice(_FIRST_NAMES)
        last  = rng.choice(_LAST_NAMES)
        name  = f"{first} {last}"
        dept  = rng.choice(_DEPARTMENTS)

        # tenure: freshers more likely in LOW/MODERATE
        if tier == "CRITICAL":
            tenure = round(rng.uniform(3.0, 15.0), 1)
        elif tier == "HIGH":
            tenure = round(rng.uniform(1.0, 12.0), 1)
        elif tier == "MODERATE":
            tenure = round(rng.uniform(0.5, 10.0), 1)
        else:
            tenure = round(rng.uniform(0.5, 12.0), 1)

        is_fresher = tenure < 1.5

        # Parameters calibrated per risk tier
        if tier == "CRITICAL":
            absenteeism     = round(rng.uniform(0.18, 0.40), 2)
            sentiment       = round(rng.uniform(-1.0, -0.45), 2)
            mood            = round(rng.uniform(1.0, 3.5), 1)
            manager_score   = round(rng.uniform(1.0, 4.5), 1)
            salary_pct      = rng.randint(10, 42)
            promo_gap       = round(rng.uniform(3.5, 7.0), 1)
            training        = rng.randint(0, 2)
            certifications  = rng.randint(0, 1)
            awards          = rng.randint(0, 1)
            job_searches    = rng.randint(9, 20)
            collab          = round(rng.uniform(0.10, 0.40), 2)
            meeting_part    = round(rng.uniform(0.15, 0.42), 2)
            cross_func      = rng.random() < 0.15
            outings         = rng.randint(0, 2)
            loc_match       = rng.random() < 0.30
            perf_trend      = rng.choice(_PERFORMANCE_BY_TIER["CRITICAL"])
            weekly_hours    = round(rng.uniform(55.0, 68.0), 1)
        elif tier == "HIGH":
            absenteeism     = round(rng.uniform(0.10, 0.22), 2)
            sentiment       = round(rng.uniform(-0.55, -0.10), 2)
            mood            = round(rng.uniform(3.0, 5.5), 1)
            manager_score   = round(rng.uniform(3.5, 6.0), 1)
            salary_pct      = rng.randint(25, 55)
            promo_gap       = round(rng.uniform(2.5, 5.0), 1)
            training        = rng.randint(1, 4)
            certifications  = rng.randint(0, 2)
            awards          = rng.randint(0, 2)
            job_searches    = rng.randint(4, 12)
            collab          = round(rng.uniform(0.35, 0.60), 2)
            meeting_part    = round(rng.uniform(0.35, 0.65), 2)
            cross_func      = rng.random() < 0.40
            outings         = rng.randint(1, 4)
            loc_match       = rng.random() < 0.55
            perf_trend      = rng.choice(_PERFORMANCE_BY_TIER["HIGH"])
            weekly_hours    = round(rng.uniform(48.0, 58.0), 1)
        elif tier == "MODERATE":
            absenteeism     = round(rng.uniform(0.04, 0.14), 2)
            sentiment       = round(rng.uniform(-0.20, 0.25), 2)
            mood            = round(rng.uniform(4.5, 7.0), 1)
            manager_score   = round(rng.uniform(5.5, 7.8), 1)
            salary_pct      = rng.randint(40, 70)
            promo_gap       = round(rng.uniform(1.5, 3.5), 1)
            training        = rng.randint(2, 5)
            certifications  = rng.randint(1, 3)
            awards          = rng.randint(1, 3)
            job_searches    = rng.randint(1, 6)
            collab          = round(rng.uniform(0.55, 0.75), 2)
            meeting_part    = round(rng.uniform(0.55, 0.78), 2)
            cross_func      = rng.random() < 0.60
            outings         = rng.randint(2, 6)
            loc_match       = rng.random() < 0.75
            perf_trend      = rng.choice(_PERFORMANCE_BY_TIER["MODERATE"])
            weekly_hours    = round(rng.uniform(42.0, 48.0), 1)
        else:  # LOW
            absenteeism     = round(rng.uniform(0.00, 0.06), 2)
            sentiment       = round(rng.uniform(0.25, 1.00), 2)
            mood            = round(rng.uniform(6.5, 10.0), 1)
            manager_score   = round(rng.uniform(7.0, 10.0), 1)
            salary_pct      = rng.randint(55, 95)
            promo_gap       = round(rng.uniform(0.5, 2.0), 1)
            training        = rng.randint(4, 10)
            certifications  = rng.randint(2, 6)
            awards          = rng.randint(2, 8)
            job_searches    = rng.randint(0, 3)
            collab          = round(rng.uniform(0.72, 1.00), 2)
            meeting_part    = round(rng.uniform(0.70, 1.00), 2)
            cross_func      = rng.random() < 0.85
            outings         = rng.randint(4, 10)
            loc_match       = rng.random() < 0.90
            perf_trend      = rng.choice(_PERFORMANCE_BY_TIER["LOW"])
            weekly_hours    = round(rng.uniform(38.0, 44.0), 1)

        feedback = rng.choice(_FEEDBACK_TEMPLATES[tier]).format(tenure=int(tenure))

        # Manager assignment logic
        if dept == "Engineering":
            if tier in ["CRITICAL", "HIGH"]:
                manager = "Tarun Gupta (Manager)" if rng.random() < 0.70 else rng.choice(["Suresh Patil (Manager)", "Rakesh Sharma (Manager)"])
            else:
                manager = rng.choice(["Suresh Patil (Manager)", "Rakesh Sharma (Manager)"])
        elif dept == "Operations":
            manager = "Amit Verma (Manager)" if rng.random() < 0.65 else "Deepak Joshi (Manager)"
        elif dept == "Product":
            manager = "Sneha Roy (Director)"
        elif dept == "Sales":
            manager = "Rajesh Kumar (Manager)"
        elif dept == "Finance":
            manager = "Anjali Menon (Manager)"
        elif dept == "HR":
            manager = "Kavita Nair (Manager)"
        elif dept == "Marketing":
            manager = "Sanjay Patel (Manager)"
        elif dept == "Data Science":
            manager = "Aditya Sen (Manager)"
        elif dept == "IT":
            manager = "Neha Sharma (Manager)"
        elif dept == "Legal":
            manager = "Zara Khan (Manager)"
        elif dept == "Customer Success":
            manager = "Bhavesh Desai (Manager)"
        else:
            manager = "Executive Management"

        employees[emp_id] = {
            "name": name,
            "department": dept,
            "manager": manager,
            "tenure_years": tenure,
            "is_fresher": is_fresher,
            "base_location_match": loc_match,
            "salary_percentile": salary_pct,
            "performance_trend": perf_trend,
            "absenteeism_rate": absenteeism,
            "meeting_participation": meeting_part,
            "collaboration_index": collab,
            "manager_scorecard": manager_score,
            "years_since_promotion": promo_gap,
            "training_count_ytd": training,
            "certifications": certifications,
            "awards_count": awards,
            "internal_job_searches": job_searches,
            "cross_functional_work": cross_func,
            "team_outings_attended": outings,
            "sentiment_score": sentiment,
            "feedback": feedback,
            "mood_index": mood,
            "weekly_hours": weekly_hours,
        }

    return employees


EMPLOYEES = _generate_employees()


# Retention actions mapped to each signal driver
DRIVER_ACTIONS = {
    "absenteeism": [
        "Schedule a confidential wellness check-in within 7 days",
        "Refer to Employee Assistance Program (EAP) for burnout support",
        "Review workload with line manager — check for overloading",
    ],
    "performance_trend": [
        "Initiate structured performance improvement dialogue (not punitive)",
        "Assign a senior mentor or buddy from high-performing peers",
        "Set clear 30-60-90 day goals collaboratively with manager",
    ],
    "compensation_gap": [
        "Trigger immediate compensation benchmarking review with HR-ADMIN",
        "Present market salary data to leadership for approval",
        "Consider spot bonus or retention bonus tied to 6-month milestone",
    ],
    "internal_job_searches": [
        "Schedule career pathing conversation this week",
        "Present internal mobility options (lateral/upward movement)",
        "Connect with internal talent marketplace for cross-team opportunities",
    ],
    "sentiment_score": [
        "Anonymous 1-on-1 feedback session with skip-level manager",
        "Deploy targeted pulse survey to understand root concerns",
        "Review team dynamics and psychological safety indicators",
    ],
    "manager_scorecard": [
        "Escalate to HR Business Partner for manager coaching intervention",
        "Review manager-employee pairing — consider team transfer if toxic",
        "Implement structured weekly 1-on-1 with clear agenda and notes",
    ],
    "promotion_gap": [
        "Initiate formal Career Development Plan (CDP) immediately",
        "Identify upcoming promotion cycle eligibility and fast-track if qualified",
        "Assign high-visibility stretch project or leadership opportunity",
    ],
    "meeting_participation": [
        "Review meeting load — eliminate non-essential meetings",
        "Check for inclusion barriers (remote/timezone/language)",
        "Manager to actively involve employee in key discussions and decisions",
    ],
    "collaboration_index": [
        "Facilitate structured team integration activities",
        "Assign collaborative project with peer buddy from another team",
        "Review whether role has sufficient cross-team touchpoints",
    ],
    "training_activity": [
        "Enroll in next available relevant certification/course immediately",
        "Allocate dedicated learning time (20% time or 4 hrs/week policy)",
        "Create personalized L&D plan for next quarter with manager sign-off",
    ],
    "recognition_count": [
        "Immediate peer shout-out recognition in next team meeting",
        "Nominate for quarterly Star Performer recognition program",
        "Manager to provide specific written appreciation (email + HR record)",
    ],
    "location_mismatch": [
        "Discuss hybrid/remote arrangement possibilities for home city visits",
        "Facilitate relocation assistance or home travel allowance if feasible",
        "Connect with local employee resource group for community building",
    ],
    "cross_functional_work": [
        "Identify cross-functional project opportunities with 2 other teams",
        "Introduce to cross-team leads for collaboration within 30 days",
    ],
    "team_social": [
        "Organize next team outing/virtual coffee within 2 weeks",
        "Include in next informal team activity — ensure they feel invited",
    ],
    "long_working_hours": [
        "Implement mandatory cap on weekend overtime",
        "Redistribute project workload across other team members",
        "Introduce flexible scheduling or compensatory time off",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# WEIGHTED RISK SCORE FORMULA
# ─────────────────────────────────────────────────────────────────────────────
def _calculate_score(emp: dict) -> dict:
    """
    Computes weighted Attrition Risk Score across 15 parameters.
    Returns total score and per-parameter breakdown.
    """
    breakdown = {}

    # 1. Absenteeism (10%)
    breakdown["absenteeism"] = round(min(emp["absenteeism_rate"] / 0.25, 1.0) * 10, 2)
    # 2. Sentiment (9%)
    breakdown["sentiment_score"] = round((1 - (emp["sentiment_score"] + 1) / 2) * 9, 2)
    # 3. Performance trend (9%)
    perf_map = {
        "high_performer": 0.0, "improving": 0.2, "stable": 0.45,
        "declining": 0.8, "low_performer": 1.0,
    }
    breakdown["performance_trend"] = round(perf_map.get(emp["performance_trend"], 0.5) * 9, 2)
    # 4. Compensation gap (9%)
    breakdown["compensation_gap"] = round((1 - emp["salary_percentile"] / 100) * 9, 2)
    # 5. Internal job searches (8%)
    breakdown["internal_job_searches"] = round(min(emp["internal_job_searches"] / 15, 1.0) * 8, 2)
    # 6. Manager scorecard (8%) — lower score = higher risk
    breakdown["manager_scorecard"] = round((1 - emp["manager_scorecard"] / 10) * 8, 2)
    # 7. Promotion gap (8%)
    breakdown["promotion_gap"] = round(min(emp["years_since_promotion"] / 5, 1.0) * 8, 2)
    # 8. Meeting participation (6%)
    breakdown["meeting_participation"] = round((1 - emp["meeting_participation"]) * 6, 2)
    # 9. Collaboration index (6%)
    breakdown["collaboration_index"] = round((1 - emp["collaboration_index"]) * 6, 2)
    # 10. Training activity (6%)
    breakdown["training_activity"] = round(max(0.0, 1 - emp["training_count_ytd"] / 8) * 6, 2)
    # 11. Recognition count (6%)
    breakdown["recognition_count"] = round(max(0.0, 1 - emp["awards_count"] / 5) * 6, 2)
    # 12. Location mismatch for freshers (5%)
    breakdown["location_mismatch"] = 5.0 if (emp["is_fresher"] and not emp["base_location_match"]) else 0.0
    # 13. Cross-functional work (3%)
    breakdown["cross_functional_work"] = 0.0 if emp["cross_functional_work"] else 3.0
    # 14. Team social engagement (2%)
    breakdown["team_social"] = round(max(0.0, 1 - emp["team_outings_attended"] / 8) * 2, 2)
    # 15. Long Working Hours (5%)
    weekly_hours = emp.get("weekly_hours", 40.0)
    breakdown["long_working_hours"] = round(min(max(0.0, weekly_hours - 40) / 20, 1.0) * 5, 2)

    total = round(min(sum(breakdown.values()), 100.0), 1)
    return {"total": total, "breakdown": breakdown}


def _get_level(score: float) -> str:
    if score >= 80.0:
        return "CRITICAL"
    elif score >= 60.0:
        return "HIGH"
    elif score >= 30.0:
        return "MODERATE"
    else:
        return "LOW"


def _get_prediction_window(level: str) -> str:
    return {
        "CRITICAL": "High probability of leaving within 3 months",
        "HIGH": "Elevated attrition risk within 6 months",
        "MODERATE": "Moderate risk — potential attrition within 12 months",
        "LOW": "Stable — monitor quarterly",
    }.get(level, "Unknown")


# ─────────────────────────────────────────────────────────────────────────────
# MCP TOOLS
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_employee_data(employee_id: str) -> str:
    """
    Retrieve full employee profile with all 14 attrition signal parameters.

    Args:
        employee_id: Employee ID string (e.g., 'EMP001')

    Returns:
        JSON string with complete employee profile and all signal parameters.
        Returns error JSON if employee not found.
    """
    emp_id = employee_id.strip().upper()
    if emp_id not in EMPLOYEES:
        available = list(EMPLOYEES.keys())
        return json.dumps({
            "error": f"Employee '{emp_id}' not found.",
            "available_ids": available,
        })
    emp = EMPLOYEES[emp_id].copy()
    # Include the employee_id in the response
    emp["employee_id"] = emp_id
    return json.dumps(emp, ensure_ascii=False)


@mcp.tool()
def compute_risk_score(employee_id: str) -> str:
    """
    Compute the weighted Attrition Risk Score for an employee using 14 signal parameters.

    Args:
        employee_id: Employee ID string (e.g., 'EMP001')

    Returns:
        JSON string with risk score, level, prediction window, parameter breakdown,
        and top 5 risk drivers sorted by contribution.
    """
    emp_id = employee_id.strip().upper()
    if emp_id not in EMPLOYEES:
        return json.dumps({"error": f"Employee '{emp_id}' not found."})

    emp = EMPLOYEES[emp_id]
    result = _calculate_score(emp)
    score = result["total"]
    breakdown = result["breakdown"]
    level = _get_level(score)
    window = _get_prediction_window(level)

    # Top 5 drivers by contribution
    top_drivers = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:5]

    return json.dumps({
        "employee_id": emp_id,
        "name": emp["name"],
        "department": emp["department"],
        "manager": emp.get("manager", "Unknown"),
        "score": score,
        "level": level,
        "prediction_window": window,
        "breakdown": breakdown,
        "top_drivers": [{"parameter": k, "contribution": v} for k, v in top_drivers],
    }, ensure_ascii=False)


@mcp.tool()
def analyze_sentiment(feedback_text: str) -> str:
    """
    Perform NLP sentiment analysis on employee feedback text.
    Detects emotional themes and mood label.

    Args:
        feedback_text: Employee feedback or survey response text

    Returns:
        JSON string with sentiment score (-1 to +1), mood label, detected themes,
        and magnitude.
    """
    text = feedback_text.lower()

    negative_keywords = [
        "burned out", "done", "disengaged", "leaving", "no growth", "undervalued",
        "ignored", "miss", "difficult", "unfair", "looking elsewhere", "not happy",
        "disconnected", "invisible", "no recognition", "stagnant", "toxic",
        "overworked", "dismissed", "don't care", "does not care", "searching",
        "other options", "no change", "nothing has changed",
    ]
    positive_keywords = [
        "excited", "love", "great", "motivated", "happy", "learning", "growing",
        "fantastic", "best", "supportive", "amazing", "excellent", "proud",
        "engaged", "thriving", "passionate", "inspired", "valued", "recognised",
        "growth", "opportunity", "career", "appreciate",
    ]

    score = 0.0
    for kw in positive_keywords:
        if kw in text:
            score += 0.15
    for kw in negative_keywords:
        if kw in text:
            score -= 0.15
    score = round(max(-1.0, min(1.0, score)), 3)

    # Theme detection
    themes_map = {
        "burnout": ["burned out", "exhausted", "done", "tired", "overworked", "no energy"],
        "career_stagnation": ["no growth", "no promotion", "stuck", "stagnant", "no change", "nothing has changed"],
        "compensation_dissatisfaction": ["salary", "compensation", "underpaid", "not reflected", "not kept up"],
        "manager_conflict": ["manager", "management", "boss", "leadership", "ignored", "dismissive", "does not care"],
        "team_disconnect": ["disconnected", "outsider", "alone", "invisible", "feel like"],
        "relocation_stress": ["miss", "hometown", "family", "far", "location", "home"],
        "job_seeking": ["looking elsewhere", "searching", "other options", "leaving", "search"],
    }
    detected_themes = [
        theme for theme, keywords in themes_map.items()
        if any(kw in text for kw in keywords)
    ]

    # Mood label
    if score >= 0.4:
        mood = "Engaged"
    elif score >= 0.1:
        mood = "Neutral-Positive"
    elif score >= -0.09:
        mood = "Neutral"
    elif score >= -0.39:
        mood = "Disengaged"
    elif score >= -0.6:
        mood = "Dissatisfied"
    else:
        mood = "Severely Disengaged"

    return json.dumps({
        "score": score,
        "mood": mood,
        "themes": detected_themes,
        "magnitude": round(abs(score), 3),
    })


@mcp.tool()
def get_retention_playbook(risk_level: str, key_drivers: list) -> str:
    """
    Generate a retention intervention playbook based on risk level and top signal drivers.

    Args:
        risk_level: One of CRITICAL, HIGH, MODERATE, LOW
        key_drivers: List of parameter names that are the top risk contributors
                     (e.g., ['absenteeism', 'manager_scorecard', 'compensation_gap'])

    Returns:
        JSON string with prioritized retention actions, owner, timeline, and urgency prefix.
    """
    level = risk_level.upper().strip()

    # Urgency prefix based on risk level
    prefix_map = {
        "CRITICAL": "🚨 URGENT: ",
        "HIGH": "⚠️ PRIORITY: ",
        "MODERATE": "📋 RECOMMENDED: ",
        "LOW": "💡 ADVISORY: ",
    }
    prefix = prefix_map.get(level, "📋 ")

    timeline_map = {
        "CRITICAL": "1–2 weeks",
        "HIGH": "1 month",
        "MODERATE": "1 quarter",
        "LOW": "Next review cycle",
    }
    priority_map = {
        "CRITICAL": "URGENT",
        "HIGH": "HIGH",
        "MODERATE": "STANDARD",
        "LOW": "ADVISORY",
    }

    actions = []
    drivers_addressed = []
    for driver in key_drivers:
        driver_key = driver.lower().strip()
        if driver_key in DRIVER_ACTIONS:
            for action in DRIVER_ACTIONS[driver_key]:
                actions.append(f"{prefix}{action}")
            drivers_addressed.append(driver_key)

    # Deduplicate while preserving order
    seen = set()
    unique_actions = []
    for a in actions:
        if a not in seen:
            seen.add(a)
            unique_actions.append(a)

    return json.dumps({
        "risk_level": level,
        "priority": priority_map.get(level, "STANDARD"),
        "timeline": timeline_map.get(level, "1 quarter"),
        "actions": unique_actions,
        "drivers_addressed": drivers_addressed,
    }, ensure_ascii=False)


@mcp.tool()
def get_department_summary(department: str) -> str:
    """
    Get aggregate attrition risk summary for an entire department.
    Shows risk distribution and top at-risk employees.

    Args:
        department: Department name (e.g., 'Engineering', 'Sales', 'Product', 'HR', 'Finance')

    Returns:
        JSON string with dept risk summary, distribution, avg score, and top at-risk employees.
    """
    dept = department.strip().title()

    # Filter employees by department
    dept_employees = {
        eid: emp for eid, emp in EMPLOYEES.items()
        if emp["department"].lower() == dept.lower()
    }

    if not dept_employees:
        all_depts = list({emp["department"] for emp in EMPLOYEES.values()})
        return json.dumps({
            "error": f"Department '{department}' not found.",
            "available_departments": sorted(all_depts),
        })

    # Compute risk scores for all employees
    scored = []
    for eid, emp in dept_employees.items():
        result = _calculate_score(emp)
        score = result["total"]
        level = _get_level(score)
        scored.append({
            "employee_id": eid,
            "name": emp["name"],
            "score": score,
            "level": level,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    # Aggregate statistics
    scores = [s["score"] for s in scored]
    avg_score = round(sum(scores) / len(scores), 1)
    avg_level = _get_level(avg_score)

    distribution = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
    for s in scored:
        distribution[s["level"]] += 1

    # Heatmap color
    color_map = {
        "CRITICAL": "#ef4444",
        "HIGH": "#f97316",
        "MODERATE": "#eab308",
        "LOW": "#22c55e",
    }

    return json.dumps({
        "department": dept,
        "employee_count": len(scored),
        "avg_risk_score": avg_score,
        "avg_risk_level": avg_level,
        "distribution": distribution,
        "top_at_risk": scored[:3],
        "all_employees": scored,
        "dept_risk_heatmap_color": color_map.get(avg_level, "#6b7280"),
    }, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")
