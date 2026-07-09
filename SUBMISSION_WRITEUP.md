# AttriSense AI — Hackathon Submission Writeup
## LTTS Global Hackathon 2026 | AI/ML Track

---

## 1. Project Title

**AttriSense AI: Predictive Employee Attrition Intelligence and Early Leaver Detection Platform**

---

## 2. Problem Statement

Employee attrition costs organizations **6–9 months of an employee's salary** per departure (SHRM). For a company of 1,000 employees with 15% annual attrition and ₹10L average salary, that's **₹9–13 crore in annual replacement costs** — excluding lost knowledge and team disruption.

The core problem: **Organizations react to attrition rather than predicting it.** By the time an employee submits their resignation, retention opportunities have passed. Early signals — declining engagement, increased absenteeism, internal job searches, manager conflicts — often appear 3–6 months before resignation. These signals exist in HR data, but no system synthesizes them proactively.

---

## 3. Proposed Solution

**AttriSense AI** is a multi-agent AI platform that continuously monitors 14 behavioral, engagement, and workplace signals to compute real-time Attrition Risk Scores and generate proactive retention interventions.

### Key Differentiators

| Aspect | Traditional HR Analytics | AttriSense AI |
|---|---|---|
| Detection | Reactive (post-resignation) | Proactive (3–6 months early) |
| Analysis | Rule-based reports | AI-powered multi-agent intelligence |
| Signals | 3–5 KPIs | 14 behavioral parameters |
| Intervention | Generic advice | Personalized, ranked retention plans |
| Security | Basic auth | PII scrubbing + injection protection + RBAC |
| Interface | Static dashboards | Conversational AI + live dashboard |

---

## 4. Technical Implementation

### 4.1 Architecture

AttriSense AI is built on **Google Agent Development Kit (ADK) 2.4.0** with a multi-agent orchestration pattern:

```
User Query → attrisense_orchestrator (LlmAgent)
                    ├── security_callback (before_model_callback)
                    │     ├── PII scrubbing
                    │     ├── Prompt injection detection  
                    │     └── Role-based access control
                    │
                    ├── signal_detection_agent (LlmAgent + MCP tools)
                    ├── sentiment_analysis_agent (LlmAgent + MCP tools)
                    ├── risk_scoring_agent (LlmAgent + MCP tools)
                    └── retention_advisor_agent (LlmAgent + MCP tools)
                              │
                    MCP Server (HR Data + Analytics Tools)
```

### 4.2 The 14-Parameter Risk Model

The Attrition Risk Score is computed as a weighted sum of 14 parameters:

| Parameter | Weight | Rationale |
|---|---|---|
| Internal Job Searches | 15% | Strongest predictor of active job seeking |
| Sentiment Score | 12% | Emotional disengagement leads to exit |
| Absenteeism Rate | 10% | Physical disengagement signal |
| Manager Scorecard | 10% | "People leave managers, not companies" |
| Promotion Gap | 10% | Career stagnation drives attrition |
| Performance Trend | 8% | Declining performers seek exit |
| Salary Percentile | 8% | Compensation mismatch for high performers |
| Collaboration Index | 7% | Social isolation precedes departure |
| Training Count | 5% | Investment in growth affects loyalty |
| Overtime Hours | 5% | Burnout signal |
| Mood Index | 5% | Daily engagement indicator |
| Awards Count | 2% | Recognition affects engagement |
| Leave Balance | 2% | Unused leave before departure |
| Location Match | 1% | Relocation friction |

**Risk Tiers:**
- 🔴 **CRITICAL** (>80%): Immediate intervention, likely departure within 3 months
- 🟠 **HIGH** (60-80%): Escalation needed, risk within 6 months
- 🟡 **MODERATE** (40-60%): Proactive monitoring, risk within 12 months
- 🟢 **LOW** (<40%): Stable, quarterly check-in

### 4.3 Multi-Agent Workflow

Each specialist agent has a focused responsibility:

**Signal Detection Agent**
- Connects to MCP server via Model Context Protocol
- Retrieves all 14 parameters for the target employee
- Applies traffic-light ratings (🔴/🟠/🟡/🟢) to each signal
- Identifies TOP 3 risk drivers

**Sentiment Analysis Agent**
- Processes employee feedback/pulse survey text
- Detects mood themes: burnout, career_stagnation, manager_conflict, work_life_balance, compensation_concern
- Generates empathetic, actionable interpretation
- Provides mood label and numeric score (-1 to +1)

**Risk Scoring Agent**
- Calls `compute_risk_score` MCP tool for weighted calculation
- Determines risk tier and prediction window
- Ranks top 5 contributing factors with percentage contributions
- Provides the "KEY INSIGHT" — the single most important pattern

**Retention Advisor Agent**
- Calls `get_retention_playbook` MCP tool
- Generates 3 PRIORITY ACTIONS with owner, timeline, expected impact
- Projects post-intervention risk reduction percentage
- Actions are specific, not generic (e.g., "Schedule career development conversation with manager by Friday" not "Improve communication")

### 4.4 Security Architecture

Security is implemented as an ADK `before_model_callback` on the orchestrator:

1. **PII Auto-Scrubbing**: Employee IDs, emails, phone numbers, salary figures, and Aadhaar numbers are redacted before any LLM processing
2. **Prompt Injection Detection**: 12 attack patterns blocked (e.g., "ignore previous instructions", "jailbreak", "reveal salary")
3. **Role Authorization**: Three roles — HR_ADMIN (full access), MANAGER (team-scoped), HR_ANALYST (salary masked)
4. **Audit Logging**: Every request logged to session state with timestamp, role, event type, and severity

### 4.5 Model Context Protocol (MCP) Integration

The MCP server (`app/mcp_server.py`) provides 4 tools:

| Tool | Description |
|---|---|
| `get_employee_data` | Returns complete 14-parameter profile for any employee |
| `analyze_sentiment` | NLP analysis of feedback text with theme detection |
| `compute_risk_score` | Weighted attrition risk calculation |
| `get_retention_playbook` | Returns personalized retention strategies by risk level and drivers |

### 4.6 HR Dashboard

A separate FastAPI application provides:
- **KPI Cards**: Total employees, Critical/High/Moderate/Low counts
- **Department Heatmap**: Average risk by department with color coding
- **Risk Distribution Chart**: Donut chart of overall risk population split
- **Employee Risk Register**: Sortable table with live scores and risk levels
- **REST API**: `/api/risk-overview`, `/api/department-heatmap`, `/api/employee/{id}`

---

## 5. Innovation Highlights

### 5.1 Proactive vs Reactive
Traditional HR analytics show what happened. AttriSense AI predicts what *will* happen — giving HR teams a 3–6 month window to intervene.

### 5.2 Multi-Agent Specialization
Each AI agent is an expert in its domain (signals, sentiment, risk, retention). This produces better results than a single monolithic prompt because each agent's context window is focused, its tools are scoped, and its outputs are structured.

### 5.3 Conversational HR Intelligence
Instead of static dashboards, HR teams can ask natural language questions:
- "Who is our highest attrition risk in Engineering?"
- "What happened to EMP001's performance last quarter?"
- "Generate a retention plan for all HIGH risk employees"

### 5.4 Safety by Design
Unlike most LLM applications, AttriSense AI treats security as a first-class citizen — not an afterthought. PII scrubbing, injection protection, and role-based access are architectural decisions, not add-ons.

---

## 6. Impact & Business Value

### For LTTS (as a use case)
- **Total Annual Attrition Cost**: **$34.5M – $51.75M per year** based on 15% attrition (approx. 3,450 exits/year) and SHRM replacement cost average ($10,000–$15,000 per employee).
- **Estimated Annual Savings (ROI)**:
  - **Conservative (5% exits prevented)**: **$1.72M – $2.58M** per year.
  - **Moderate (10% exits prevented)**: **$3.45M – $5.17M** per year.
  - **Optimistic (15% exits prevented)**: **$5.17M – $7.75M** per year.
- **System Cost vs Value**: Total annual cost of AttriSense AI is ~$12,000 (API and cloud hosting), yielding a **35x to 100x return on investment (ROI)**.
- **HR productivity**: Automated multi-agent intelligence replaces 60+ hours/month of manual risk assessment and report compilation.

### Scalability
- Works for any company with HR data
- Configurable parameters and weights
- Department-level and individual-level analysis
- Extensible to other HR systems via MCP

---

## 7. Technical Stack

| Layer | Technology | Version |
|---|---|---|
| AI Framework | Google Agent Development Kit (ADK) | 2.4.0 |
| LLM | Google Gemini 2.5 Flash | Latest |
| Tool Protocol | Model Context Protocol (MCP) | 1.x |
| Web Framework | FastAPI | 0.115+ |
| ASGI Server | Uvicorn | 0.32+ |
| Package Manager | uv | Latest |
| Language | Python | 3.12 |

---

## 8. Demo Script

**Scenario: LTTS Engineering Manager receives an alert about EMP001**

1. Open ADK Playground: `http://127.0.0.1:18081/dev-ui/?app=app`
2. Type: `analyze EMP001`
3. Agent sequence runs:
   - Signal Detection Agent → fetches 14 parameters
   - Sentiment Analysis Agent → analyzes feedback
   - Risk Scoring Agent → computes weighted score
   - Retention Advisor Agent → generates action plan
4. Receive structured report with CRITICAL risk alert
5. Open HR Dashboard: `http://127.0.0.1:18082/`
6. View department heatmap — Engineering shows 68.1% HIGH risk
7. HR manager takes action: schedule career discussion, compensation review

---

## 9. Future Roadmap

| Phase | Feature | Timeline |
|---|---|---|
| v1.1 | Integration with HRMS (SAP, Workday) | Q3 2026 |
| v1.2 | Real-time Slack/Teams alerts for HR managers | Q3 2026 |
| v2.0 | Longitudinal trend analysis (6-month rolling window) | Q4 2026 |
| v2.1 | Peer benchmark comparison across similar organizations | Q4 2026 |
| v3.0 | GCP deployment with Vertex AI and Cloud Run | Q1 2027 |
| v3.1 | Custom model fine-tuning on LTTS attrition data | Q1 2027 |

---

## 10. Repository Structure

```
attrisense-ai/
├── app/
│   ├── __init__.py          # ADK entry point
│   ├── agent.py             # Multi-agent orchestration (ADK 2.4.0)
│   ├── config.py            # Model configuration
│   ├── mcp_server.py        # MCP server with HR tools
│   └── fast_api_app.py      # HR Dashboard (FastAPI)
├── .env                     # API key (not committed)
├── pyproject.toml           # Dependencies
└── README.md                # Setup guide
```

---

*Built with ❤️ for LTTS Global Hackathon 2026 | Powered by Google ADK + Gemini 2.5 Flash*
