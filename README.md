# AttriSense AI 🧠
### Predictive Employee Attrition Intelligence & Early Leaver Detection Platform
**LTTS Global Hackathon 2026 — AI/ML Track**

> *"Predict Attrition Before It Happens."*

---

## 🚀 What is AttriSense AI?

AttriSense AI is a **multi-agent AI platform** that detects early signals of employee attrition and generates actionable HR interventions — **before** an employee submits their resignation.

Built on **Google Agent Development Kit (ADK) 2.4.0**, it orchestrates 4 specialized AI agents to analyze 14 behavioral, engagement, and workplace signals and compute a real-time **Attrition Risk Score** for every employee.

---

## 📸 Screenshots

| ADK Playground (Agent Graph) | HR Dashboard |
|---|---|
| Agent graph showing orchestrator + 4 sub-agents | Dark glassmorphism HR analytics dashboard |

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Multi-Agent AI** | 4 specialist sub-agents (Signal Detection, Sentiment, Risk Scoring, Retention) orchestrated via ADK 2.4.0 |
| 📊 **14-Parameter Risk Model** | Absenteeism, sentiment, manager scores, promotion gaps, internal job searches, and more |
| 🎯 **Attrition Risk Score** | Weighted composite score with CRITICAL / HIGH / MODERATE / LOW tiers |
| 💬 **Sentiment Analysis** | NLP-based mood analysis of employee feedback with theme detection |
| 🛡️ **Security-First Design** | PII scrubbing, prompt injection detection, HR role-based access control |
| 📋 **Retention Playbooks** | Ranked, actionable retention plans with owner, timeline, and expected impact |
| 🖥️ **Live HR Dashboard** | Real-time risk register, department heatmap, and distribution charts |
| 🔗 **MCP Integration** | Model Context Protocol server providing HR data and analytics tools |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AttriSense AI Platform                       │
│                                                                 │
│  ┌─────────────┐      ADK Web UI / HR Dashboard                │
│  │  HR Manager │ ──→  http://localhost:18081   (ADK Playground) │
│  │             │ ──→  http://localhost:18082   (HR Dashboard)   │
│  └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │             attrisense_orchestrator (LlmAgent)          │    │
│  │         Security Callback + Multi-Agent Routing         │    │
│  └────┬──────────┬──────────┬──────────┬──────────────────┘    │
│       │          │          │          │                        │
│       ▼          ▼          ▼          ▼                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────────┐     │
│  │ Signal  │ │Sentiment│ │  Risk   │ │    Retention     │     │
│  │Detection│ │Analysis │ │ Scoring │ │    Advisor       │     │
│  │ Agent   │ │ Agent   │ │ Agent   │ │    Agent         │     │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────────┬─────────┘     │
│       │           │           │               │                │
│       └───────────┴───────────┴───────────────┘                │
│                           │                                    │
│                           ▼                                    │
│              ┌────────────────────────┐                        │
│              │   MCP Server (stdio)   │                        │
│              │  HR Data + Analytics   │                        │
│              │  Tools via MCP Protocol│                        │
│              └────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role |
|---|---|
| **attrisense_orchestrator** | Root agent: routes queries, coordinates sub-agents, produces final report |
| **signal_detection_agent** | Retrieves 14 behavioral signals, applies traffic-light rating |
| **sentiment_analysis_agent** | Analyzes employee feedback text for mood, themes, and engagement |
| **risk_scoring_agent** | Computes weighted Attrition Risk Score and prediction window |
| **retention_advisor_agent** | Generates ranked, actionable retention intervention plan |

---

## 📡 The 14 Signal Parameters

| # | Signal | Risk Threshold |
|---|---|---|
| 1 | Absenteeism Rate | > 15% → HIGH |
| 2 | Performance Trend | Declining 2 qtrs → HIGH |
| 3 | Manager Scorecard | < 5.0/10 → HIGH |
| 4 | Promotion Gap (years) | > 3 years → HIGH |
| 5 | Training Count | < 2/year → WARNING |
| 6 | Internal Job Searches | > 8 → CRITICAL |
| 7 | Collaboration Index | < 0.50 → WARNING |
| 8 | Sentiment Score | < -0.3 → HIGH |
| 9 | Salary Percentile | < 40% (High performer) → FLIGHT RISK |
| 10 | Mood Index | < 3.0 → WARNING |
| 11 | Awards Count | 0 in 12 months → WARNING |
| 12 | Location Match | Mismatch + fresher → HIGH |
| 13 | Overtime Hours/Week | > 20 → HIGH |
| 14 | Leave Balance | High unused → MODERATE |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- uv package manager
- Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Installation

```bash
# 1. Clone the repository
cd "LTTS Vad Hackathon 26 July/adk-workspace/attrisense-ai"

# 2. Create .env file
echo "GOOGLE_API_KEY=your_key_here
GOOGLE_GENAI_USE_VERTEXAI=False
GEMINI_MODEL=gemini-2.5-flash" > .env

# 3. Install dependencies
uv sync

# 4. Launch ADK Playground
uv run adk web app --host 127.0.0.1 --port 18081

# 5. Launch HR Dashboard (new terminal)
uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 18082
```

### Access

| Service | URL |
|---|---|
| 🤖 ADK Playground (Agent Chat) | http://127.0.0.1:18081/dev-ui/?app=app |
| 📊 HR Dashboard | http://127.0.0.1:18082/ |
| 🔌 API | http://127.0.0.1:18082/api/risk-overview |

---

## 💬 Demo Queries

Try these in the ADK Playground:

```
analyze EMP001
analyze the Engineering department  
Who are our highest attrition risks right now?
What are the top retention strategies for high performers?
```

---

## 🗂️ Project Structure

```
attrisense-ai/
├── app/
│   ├── __init__.py          # ADK entry point (exports `app`)
│   ├── agent.py             # Multi-agent orchestration (ADK 2.4.0)
│   ├── config.py            # Model & configuration settings
│   ├── mcp_server.py        # MCP server: HR data + analytics tools
│   └── fast_api_app.py      # HR Dashboard + REST API
├── .env                     # API key configuration
├── pyproject.toml           # Project dependencies
└── README.md
```

---

## 🛡️ Security Features

- **PII Scrubbing**: Employee IDs, emails, phone numbers, salaries, Aadhaar numbers are automatically redacted
- **Prompt Injection Protection**: 12+ attack patterns blocked with audit logging
- **Role-Based Access**: HR_ADMIN / MANAGER / HR_ANALYST with salary masking for analysts
- **Audit Trail**: Every request is logged with timestamp, role, and event type

---

## 🔧 Technology Stack

| Component | Technology |
|---|---|
| AI Framework | Google ADK 2.4.0 |
| LLM | Gemini 2.5 Flash |
| Tool Protocol | Model Context Protocol (MCP) |
| API Framework | FastAPI + Uvicorn |
| Package Manager | uv |
| Python | 3.12 |

---

## 👥 Team

**LTTS Global Hackathon 2026**
Built with ❤️ using Google Agent Development Kit

---

## 📄 License

Apache 2.0 — See LICENSE for details.
