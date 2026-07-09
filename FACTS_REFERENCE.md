# AttriSense AI — Key Facts Reference Document
## For All Jury Rounds | LTTS Global Hackathon 2026

---

## 👥 Team Composition

| Member | Background | Experience | Role in Project |
|---|---|---|---|
| **CSE Engineer** | Computer Science | 5+ years | Architecture, AI agents, MCP, backend development |
| **GET #1** | Mechanical Engineering | 1–2 years | Problem domain, HR research, parameter design |
| **GET #2** | Electrical Engineering | 1–2 years | Market research, competitive analysis, business case |
| **GET #3** | Mechanical / Electrical | 1–2 years | Product design, dashboard UX, user testing |

> **Jury pitch:** *"Three of our four members are non-CSE engineers. They defined the problem. The CSE engineer built what they described. That is exactly how enterprise products should be built — domain expertise driving technical decisions."*

---

## 📉 Attrition Rate Facts

### LTTS Attrition Rate (Publicly Available Data)
| Period | Rate | Context |
|---|---|---|
| FY2022–23 | ~17–19% | Post-COVID attrition surge across IT sector |
| FY2023–24 | ~13–16% | Declining trend as market stabilized |
| Typical range | 13–18% | Consistent with peer IT-engineering companies |

> ⚠️ **Verify** exact current figure from LTTS latest quarterly investor report before presenting.
> **Source:** LTTS annual reports and investor presentations (publicly available on BSE/NSE).

### Industry Benchmark Attrition Rates
| Sector | Average Annual Attrition |
|---|---|
| IT / Software (India) | 15–22% |
| Engineering Services (India) | 12–18% |
| Manufacturing (India) | 8–12% |
| BFSI / Banking (India) | 20–28% |
| Global Technology average | 13–19% |
| **Optimal / Healthy attrition target** | **8–12%** |

> **Source:** SHRM India, LinkedIn Workforce Report 2024, Mercer India Talent Trends 2024

---

## ✅ Why 10% Is the Right Target — Not 0%

This is a critical point that distinguishes a mature HR product from a naive one.

**A healthy organization needs some natural attrition because:**
1. **Retirement and life transitions** — unavoidable and natural
2. **Role outgrowth** — employees who have genuinely exceeded their ceiling need to progress or move on
3. **Performance management** — low performers eventually exiting keeps the organization healthy
4. **Fresh perspectives** — new hires bring updated skills, market knowledge, and competitor insights
5. **Cost management** — 100% retention leads to salary inflation, skill stagnation, and organizational rigidity

**The enemy is INVOLUNTARY attrition of high-value employees:**
- High performers quietly leaving because their compensation hasn't been reviewed in 3 years
- Engaged employees resigning because a toxic manager relationship was never escalated
- Talented freshers relocating away because their home-city stress signal was never picked up

> **AttriSense AI does NOT aim to eliminate attrition. It aims to eliminate SURPRISE attrition — giving LTTS 3–6 months to act before the resignation letter arrives.**

---

## 💰 ROI — Business Case in US Dollars

### The Cost of Replacing One Employee

SHRM (Society for Human Resource Management) — the global HR authority — states:
> **"Replacing one employee costs 50% to 200% of their annual salary."**

For a mid-level IT/engineering professional at LTTS (average CTC ~₹8–12 lakhs = ~$10,000–14,000/year):
- **Replacement cost = $10,000–$15,000 per person** (recruitment, onboarding, training, lost productivity)

### LTTS-Specific ROI Calculation

| Metric | Value |
|---|---|
| LTTS Total Employees (approx) | ~23,000 |
| Attrition Rate (15%) | ~3,450 exits per year |
| Average Replacement Cost | $10,000–$15,000 per employee |
| **Total Annual Attrition Cost** | **$34.5M – $51.75M per year** |

### AttriSense AI's Financial Impact

| Scenario | Involuntary Exits Prevented | **Annual Saving (USD)** |
|---|---|---|
| Conservative — save 5% of exits | ~172 employees | **$1.72M – $2.58M** |
| **Moderate — save 10% of exits** | **~345 employees** | **$3.45M – $5.17M** |
| Optimistic — save 15% of exits | ~517 employees | $5.17M – $7.75M |

> ### 💡 One-Line Jury Pitch
> *"Even at the most conservative estimate — retaining just 5% of at-risk employees — AttriSense AI saves LTTS over **$1.7 million per year**. The system pays for itself many times over in year one."*

### Return on Investment
| Cost of Building AttriSense AI | Annual Saving (moderate) | ROI |
|---|---|---|
| ~$50,000–$100,000 (development + hosting) | $3.45M–$5.17M | **35x – 100x ROI** |

---

## 📊 The 14 Parameters — Full Reference

### What is Frequency?

**Frequency** means **how often each signal is measured and updated** in the system.

Think of it like health checkups — you check blood pressure weekly, but get an MRI only if needed. Different signals naturally update at different intervals:

- **Real-time** parameters update every time an employee takes an action (e.g., clicking a job posting)
- **Monthly** parameters are pulled from payroll/attendance systems at the end of each month
- **Quarterly** parameters come from structured review cycles
- **Annual** parameters come from yearly benchmarking exercises

---

### What is Threshold?

**Threshold** means **the specific value at which a parameter starts flagging as a risk signal**.

Think of it like a traffic signal:
- Below threshold = 🟢 Green — normal, no concern
- At threshold = 🟡 Yellow — watch this employee
- Above threshold = 🔴 Red — this parameter is actively contributing to attrition risk

Every parameter has its own threshold based on HR research and industry standards. When multiple parameters cross their thresholds simultaneously, the combined risk score escalates rapidly toward CRITICAL.

---

### The 14 Parameters — Frequency, Threshold, and Plain English Meaning

| # | Parameter | Weight | Frequency | Safe Zone | ⚠️ Warning | 🔴 High Risk Threshold |
|---|---|---|---|---|---|---|
| 1 | **Absenteeism Rate** | 12% | Monthly | < 5% absence | 5–15% | **> 15%** of working days missed |
| 2 | **Sentiment Score** | 10% | Quarterly | > +0.2 | 0 to −0.2 | **< −0.3** (negative NLP score on feedback) |
| 3 | **Performance Trend** | 10% | Quarterly | High Performer / Improving | Stable | **Declining / Low Performer** |
| 4 | **Compensation Gap** | 10% | Annual | > 60th percentile | 40th–60th | **< 40th percentile** vs market |
| 5 | **Internal Job Searches** | 8% | Real-time | 0–2 per month | 3–5 per month | **> 5 per month** |
| 6 | **Manager Scorecard** | 8% | Quarterly | > 7.0 / 10 | 5.0–7.0 | **< 5.0 / 10** (poor manager relationship) |
| 7 | **Promotion Gap** | 8% | Continuous | < 2 years | 2–3 years | **> 3 years** without any promotion |
| 8 | **Meeting Participation** | 6% | Weekly | > 70% | 50–70% | **< 50%** attendance in meetings |
| 9 | **Collaboration Index** | 6% | Monthly | > 70% | 40–70% | **< 40%** cross-team project involvement |
| 10 | **Training Activity** | 6% | Monthly | > 4 trainings/year | 2–4 | **0 trainings in 6 months** |
| 11 | **Recognition Count** | 6% | Continuous | ≥ 2 awards/year | 1 award/year | **0 awards in 12 months** |
| 12 | **Location Mismatch** | 5% | Once + Annual | Home city = work city | — | **Fresher relocated away from home** |
| 13 | **Cross-functional Work** | 3% | Monthly | Active cross-team projects | Occasional | **No cross-team work in 6 months** |
| 14 | **Team Social Engagement** | 2% | Monthly | ≥ 4 outings/year | 2–3 outings | **0 team outings in 6 months** |

**Total Weight = 100%**

---

### Score → Risk Level Mapping

| Composite Score | Risk Level | Meaning | Action Required |
|---|---|---|---|
| 80 – 100% | 🔴 **CRITICAL** | High probability of leaving within 3 months | Immediate — within 1–2 weeks |
| 60 – 79% | 🟠 **HIGH** | Elevated attrition risk within 6 months | Priority — within 1 month |
| 30 – 59% | 🟡 **MODERATE** | Potential attrition within 12 months | Standard — within 1 quarter |
| 0 – 29% | 🟢 **LOW** | Stable — monitor quarterly | Advisory — next review cycle |

---

### Worked Example — How Frequency and Threshold Work Together

> **Employee:** Arjun Sharma | **Department:** Engineering | **Tenure:** 4 years

| Parameter | Current Value | Threshold | Status | Contribution to Score |
|---|---|---|---|---|
| Absenteeism Rate | 22% | > 15% | 🔴 BREACH | 10.56 / 12 pts |
| Internal Job Searches | 13 / month | > 5 | 🔴 BREACH | 6.93 / 8 pts |
| Years Since Promotion | 4 years | > 3 years | 🔴 BREACH | 6.40 / 8 pts |
| Compensation Gap | 35th percentile | < 40th | 🔴 BREACH | 6.50 / 10 pts |
| Sentiment Score | −0.75 | < −0.3 | 🔴 BREACH | 8.75 / 10 pts |
| **Combined Score** | | | | **81.3% → CRITICAL** |

> *Frequency note: Absenteeism was updated last month. Job searches are real-time — we knew within 24 hours that he searched 13 times. The salary percentile was last updated at the annual compensation review. All of these together cross their thresholds simultaneously — which is why the combined score reaches CRITICAL.*

---

## 🆚 Competitive Landscape

| Platform | What They Do | What They Don't Do |
|---|---|---|
| **Workday** | Risk score only | No personalized retention plan; no NLP |
| **SAP SuccessFactors** | Workforce analytics dashboards | No AI-generated intervention recommendations |
| **Oracle HCM** | Turnover probability prediction | No 14-parameter explainability breakdown |
| **Visier** | People analytics and benchmarking | No agent-based reasoning; no real-time entry |
| **Microsoft Viva** | Collaboration signals only | No compensation or promotion gap signals |
| **IBM Watson** | ML attrition model | No personalized actions; black-box prediction |

### Our 3 Unique Differentiators vs All Competitors

1. **Explainability** — We show the exact parameter-by-parameter breakdown driving the risk. Competitors give a number. We give reasons.
2. **Personalized AI Retention Plans** — Not generic suggestions. Our Retention Advisor Agent generates specific actions tied to that employee's top 3 risk drivers, with owners and timelines.
3. **Real-time Employee Entry** — Any HR manager can add a new employee and get an instant AI risk analysis in under 30 seconds. No batch processing, no waiting for the next monthly run.

---

## 🏗️ Technical Stack

| Component | Technology | Why Chosen |
|---|---|---|
| AI Agents | Google ADK 2.4.0 | Enterprise-grade, open-source, true multi-agent orchestration |
| Language Model | Gemini 2.5 Flash | Best reasoning-to-cost ratio; strong structured output |
| Data Protocol | MCP (Model Context Protocol) | Prevents hallucination; data sources are swappable |
| HR Dashboard | FastAPI + Vanilla JS | Lightweight, fast, no frontend framework dependency |
| Security Layer | before_model_callback | PII scrubbing, prompt injection protection, RBAC |
| Dataset | 1,000 synthetic employees | Deterministic seed (42), realistic risk distributions |

---

## 🙋 Complete Q&A Cheat Sheet

**"The idea already exists — Workday, SAP all do this."**
> "Yes, and we studied all of them. The concept of attrition prediction exists. What doesn't exist — at accessible cost, with explainability and personalized AI plans — is what we built. We're not trying to compete with Workday globally. We're saying LTTS should own its attrition intelligence internally, with full data control and a fraction of the cost."

**"Why are non-CSE engineers doing an AI project?"**
> "Because LTTS's greatest strength is cross-functional engineering. Our mechanical and electrical team members defined the problem domain, researched HR literature, calibrated parameter weights based on industry studies, and user-tested the dashboard. The CSE engineer (5+ years experience) built what they described. That is exactly how good enterprise products are built."

**"What data does this use? How accurate is it?"**
> "For this demo: 1,000 synthetic employees. In production: real HRMS data via our MCP data layer — SAP, Workday, Oracle, or any system. Accuracy improves when fine-tuned on LTTS's own historical attrition data. IBM's similar model achieved 95%+ accuracy after training on real organizational data."

**"What is the accuracy of the risk score?"**
> "The 14-parameter weighted model is calibrated against published HR research (Gallup, SHRM, IBM HR study). The formula is transparent and auditable — not a black box. Production accuracy depends on calibration with LTTS historical data, which we can do in 1–2 months."

**"What happens when an employee's data changes?"**
> "Each parameter updates at its natural frequency — absenteeism monthly, sentiment quarterly, job searches real-time. The risk score recomputes automatically on every update. If someone gets promoted today, their promotion gap resets to zero and their score drops immediately. The system is always current."

**"Can employees game the system?"**
> "Individual parameters could be gamed — someone might attend more meetings artificially. But gaming all 14 cross-validated signals simultaneously is practically impossible. The system also monitors trend changes — a sudden spike in meeting attendance alongside 10 internal job searches is actually a stronger signal than either alone."

**"What about employee privacy and ethics?"**
> "Three protection layers: PII scrubbing before any data reaches the AI, role-based access control (managers see only their team), and a full audit trail of every query. The system is designed with GDPR principles in mind. The purpose is to help employees — not to surveil them. We alert HR to help, not to punish."

**"Is this production-ready?"**
> "The architecture is production-ready — ADK 2.4.0, FastAPI, MCP — all enterprise-grade. The demo uses synthetic data. Going to production requires HRMS integration (2–4 weeks) and historical data calibration (1–2 months). We estimate 3 months to full deployment at LTTS."

**"What does it cost to run?"**
> "On free-tier Gemini API: zero cost. On paid tier for 23,000 employees analyzed weekly: approximately $200–$500 per month in API costs. Infrastructure (cloud hosting): $300–$500/month. Total: under $1,000/month — against potential savings of $3.45M+ per year."

---

*AttriSense AI — Predict Attrition Before It Happens*
*LTTS Global Hackathon 2026 | Team: 1 CSE (5+ yrs) + 3 GETs (Mech/Elec)*
