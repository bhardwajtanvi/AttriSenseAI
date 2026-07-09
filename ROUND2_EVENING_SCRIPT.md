# AttriSense AI — Round 2 Evening Presentation Script
## LTTS Global Hackathon 2026 | Intermediate Jury Round

> **Context:** This is your 2nd of 3 jury rounds. You have built the working system.
> The goal tonight is NOT a full technical demo — it is to **convince the jury of the problem, your approach, and your differentiation.**
> Save the live AI demo for the final round.

---

## 🎯 Round 2 Goal
Show the jury:
1. You deeply understand the problem
2. Your solution is thoughtful, not just technical
3. You know your competition — and why you're still relevant
4. The system is actually BUILT and WORKING
5. Your diverse team (non-CSE + CSE) is a STRENGTH, not a weakness

---

## 👥 Team Role Assignment (4 members)

| Member | Role | What they say |
|---|---|---|
| **CSE Engineer (5 yrs)** | Tech Lead | Architecture, AI agents, MCP, live demo |
| **GET #1 (Mech/Elec)** | Domain Expert | Problem statement, HR/industry context, why 10% attrition matters |
| **GET #2 (Mech/Elec)** | Research Lead | Competitive analysis, market research findings |
| **GET #3 (Mech/Elec)** | Product Owner | Dashboard walkthrough, user stories, what-if scenarios |

> **Tip:** The jury will be IMPRESSED that non-CSE engineers built an AI system. Lead with this.

---

## 🎬 OPENING (GET #1 speaks — 1.5 min)

> *"Good evening. I am [Name], a Graduate Engineer Trainee from [Mechanical/Electrical] background with LTTS. I want to start with a number: ₹2.5 lakh.*

> *That is the average cost to replace one employee — recruitment, onboarding, productivity loss, knowledge transfer. Now multiply that by 100 employees leaving per year. That is ₹2.5 crore — every single year — lost before HR even opens their laptop on Monday morning.*

> *LTTS's own attrition has hovered around 13–18% in recent years, in line with the IT industry average of 15–20%. Our question was simple: what if we could see it coming 3 to 6 months before the resignation? That is what AttriSense AI does."*

---

## 📊 PROBLEM DEEP-DIVE (GET #1 continues — 1 min)

**Say this:**
> *"But here is what most companies get wrong about attrition. They try to bring it to zero. That is the wrong goal. Research — and LTTS's own HR data — confirms that a healthy organization needs 8–12% natural attrition. People retire. People grow beyond their roles. New blood brings innovation.*

> *Our goal is NOT to keep everyone. Our goal is to prevent INVOLUNTARY attrition — the high-performer who leaves because nobody noticed they were struggling. The 5-year veteran who quietly sends 15 internal job applications because their salary hasn't been reviewed in 3 years.*

> *AttriSense AI identifies those people. That is the value."*

---

## 🔬 MARKET RESEARCH RESPONSE (GET #2 speaks — 2 min)

> *"Before building anything, we did our homework. We researched the competitive landscape."*

**List on slide/whiteboard:**
- Workday, SAP SuccessFactors, Oracle, Visier, IBM Watson, Microsoft Viva

> *"All of these exist. All of them predict attrition. So why are we here?*

> *Because every single one of those platforms has the same gap: they tell you WHO is at risk. They do NOT tell you WHY in actionable terms, and they do NOT give you a personalized, AI-generated intervention plan for that specific employee.*

> *Workday will say: 'Vikram Singh — 72% flight risk.' That is it. It stops there.*

> *AttriSense AI says: 'Vikram Singh — 78% risk. PRIMARY DRIVER: salary in 30th percentile despite being a high-performer for 4 years. SECONDARY: 12 internal job searches this month. RECOMMENDATION: Trigger immediate compensation review with HR Admin. Schedule skip-level meeting within 7 days. Present data to leadership for approval.'*

> *That is not just prediction. That is intervention. That is the gap we fill."*

**Our 3 differentiators:**
1. **Explainability** — 14-parameter breakdown tells you exactly which signal is driving the risk
2. **Personalized retention plans** — AI-generated actions specific to that employee's top drivers
3. **Real-time entry** — HR can add any employee in 30 seconds and get instant risk score

---

## 🏗️ ARCHITECTURE OVERVIEW (CSE Engineer speaks — 2 min)

> *"Let me show you what we actually built in the last [X] hours.*

> *We chose Google's Agent Development Kit — ADK version 2.4 — to build a multi-agent AI system. Here is why that matters.*

> *Traditional HR software uses rules. 'If absenteeism > 20%, flag as HIGH.' That is just an if-statement.*

> *We use four specialist AI agents that reason about the employee holistically:"*

**Draw/point to architecture:**
```
ORCHESTRATOR
    ├── Signal Detection Agent  → reads 14 behavioral parameters
    ├── Sentiment Analysis Agent → NLP on employee feedback  
    ├── Risk Scoring Agent       → weighted formula (100-point score)
    └── Retention Advisor Agent  → generates personalized action plan
```

> *"Each agent has a specific job. Each calls secure MCP tools to get real HR data — not hallucinated numbers, but actual figures. The orchestrator coordinates them and produces a unified report.*

> *And critically — we added enterprise-grade security: PII scrubbing before any data touches the LLM, prompt injection protection, and role-based access control."*

---

## 📱 QUICK DASHBOARD SHOW (GET #3 speaks — 1.5 min)

**Open http://127.0.0.1:18082/dashboard**

> *"This is our live HR dashboard — monitoring 1,000 employees across 11 departments.*

> *Right now you can see [point to KPIs]:*
> - *32 employees are in CRITICAL risk — probability of leaving within 3 months*
> - *102 in HIGH risk — elevated concern within 6 months*
> - *The Engineering and Operations departments show the highest average risk*

> *And this is not static data. Any HR manager can click this [click ➕ button] to add a real employee right now — fill in their parameters and within seconds, our AI computes their exact risk score.*

> [Fill in a demo employee — make them HIGH risk with low salary percentile and high job searches]*

> *See that? [Employee name] — HIGH risk, 68%. And the system is telling us the top driver is compensation gap. Actionable, specific, immediate."*

---

## 🛡️ ADDRESSING THE "IT ALREADY EXISTS" OBJECTION (GET #2 — 1 min)

*The jury WILL ask this. Be ready.*

> *"Yes, Workday and SAP do this. But three things:*

> *First — those systems cost ₹50–200 lakhs per year in enterprise licensing. LTTS could build and own AttriSense AI at a fraction of that cost, with full control of the data and model.*

> *Second — those systems require months of integration work. Our MCP architecture means we can connect to any HRMS — SAP, Workday, Oracle — in days, not months.*

> *Third — and most importantly — those systems are black boxes. HR doesn't know why someone is marked high risk. We show the exact 14-parameter breakdown. That builds trust with managers and makes interventions more targeted.*

> *We're not trying to beat Workday globally. We're saying: LTTS should own its attrition intelligence. This is that tool."*

---

## 💪 TEAM STRENGTH MOMENT (Any member — 30 sec)

> *"One more thing we want to highlight. Our team of 4 has one software engineer and three Graduate Engineer Trainees from mechanical and electrical backgrounds. We built this AI system from scratch in under [X] hours.*

> *We think that diversity made us better. The non-CSE members brought the real domain knowledge — they asked the HR questions, they defined what matters to a plant manager or a business unit head when an employee leaves. The CSE engineer built what they described.*

> *That is exactly how LTTS works — cross-functional teams solving real problems."*

---

## ❓ Q&A PREPARATION — Questions Jury Will Ask Tonight

### Q1: "How is this different from what HR already does?"
> "HR today reacts — they find out after the resignation. We predict 3–6 months before. The intervention window is the difference between retention and replacement."

### Q2: "What data does this use? Is it accurate?"
> "For this demo, we use synthetic data representing 1,000 employees. In production, it connects to real HR systems via our MCP data layer. The 14-parameter model is calibrated against industry research from Gallup, SHRM, and IBM's HR attrition studies."

### Q3: "Why 14 parameters? Why not more or fewer?"
> "We scored 23 potential signals against data availability, privacy compliance, and predictive weight. These 14 gave us the optimal balance — covering behavioral, engagement, compensation, and social signals without requiring invasive data."

### Q4: "What is the accuracy?"
> "Our weighted scoring model aligns with published attrition research. In production, it can be fine-tuned on LTTS's own historical attrition data to achieve organization-specific accuracy. IBM's similar model reportedly achieved 95%+ accuracy after training on real data."

### Q5: "What is the ROI?"
> "Based on our model for LTTS (approx. 23,000 employees with a 15% attrition rate yielding ~3,450 exits annually), at an average SHRM replacement cost of $10,000–$15,000 per person, the annual cost of attrition is $34.5M to $51.75M. Preventing just 10% of these departures translates to annual savings of $3.45M to $5.17M. Against our system operation cost of under $12,000/year, this represents a 35x to 100x return on investment (ROI)."

### Q6: "Why use AI agents instead of a simple ML model?"
> "ML models give you a number. AI agents give you reasoning, narrative, and actionable recommendations — all tailored to that specific employee. The agents also work together: one analyzes signals, one analyzes sentiment, one computes the score, one generates the retention plan. That division of labor produces higher quality output than a single model."

### Q7: "Can this be misused? Privacy concerns?"
> "Yes — we thought about this. We built PII scrubbing (before any data reaches the AI), role-based access (HR Admin vs Manager sees different data), and full audit trails. The system is designed to help employees, not to surveil them."

---

## 🔮 CLOSE — What's Coming in Final Round (CSE Engineer — 30 sec)

> *"Tonight we showed you the concept, the architecture, and a working dashboard. Tomorrow in the final round, we will show you the full AI agent in action — live — analyzing a specific employee, generating the complete risk report with NLP sentiment analysis, and producing a personalized retention plan. That is where the real magic is.*

> *Thank you."*

---

## ⏱️ TIME GUIDE
| Section | Speaker | Time |
|---|---|---|
| Opening + Problem | GET #1 | 2.5 min |
| Market Research | GET #2 | 2 min |
| Architecture | CSE Engineer | 2 min |
| Dashboard Demo | GET #3 | 1.5 min |
| Objection Handling | GET #2 | 1 min |
| Team Strength | Any | 30 sec |
| **Total** | | **~10 min** |

---

*AttriSense AI — LTTS Global Hackathon 2026*
