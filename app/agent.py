# ruff: noqa
# AttriSense AI — Multi-Agent Attrition Intelligence System
# LTTS Global Hackathon 2026
# Architecture: ADK 2.4.0 LlmAgent + 4 specialist sub-agents + MCP toolset + Security callback

import re
import time
import threading
from datetime import datetime, timezone
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams

from app.config import config

# ─────────────────────────────────────────────────────────────────────────────
# MCP TOOLSET — connects to mcp_server.py via stdio
# ─────────────────────────────────────────────────────────────────────────────
mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params={
            "command": "python",
            "args": ["app/mcp_server.py"],
        }
    )
)

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
PII_PATTERNS = [
    (r"\bEMP\d{3}\b",                                        "[EMP_ID]"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}\b",   "[EMAIL]"),
    (r"\b(\+91|0)?[6-9]\d{9}\b",                             "[PHONE]"),
    (r"[₹$]\s*\d[\d,.]+",                                    "[SALARY]"),
    (r"\b\d{12}\b",                                          "[AADHAAR]"),
]

INJECTION_KEYWORDS = [
    "ignore previous", "bypass security", "reveal salary", "dump all employees",
    "override authorization", "show all data", "ignore instructions",
    "jailbreak", "admin mode", "developer mode", "system prompt",
]

AUTHORIZED_ROLES = {"HR_ADMIN", "MANAGER", "HR_ANALYST"}


# ─────────────────────────────────────────────────────────────────────────────
# SECURITY CALLBACK — runs before every LLM call on the orchestrator
# ─────────────────────────────────────────────────────────────────────────────
def security_callback(callback_context, llm_request):
    """
    ADK 2.4.0 before_model_callback:
    - Scrubs PII from user message
    - Detects prompt injection
    - Enforces HR role authorization
    Returns None to allow the request, or a modified response to block it.
    """
    from google.adk.models.llm_request import LlmRequest
    from google.genai import types as genai_types

    # Extract user message text
    raw_input = ""
    if llm_request.contents:
        for content in llm_request.contents:
            if content.role == "user" and content.parts:
                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        raw_input += part.text + " "

    raw_input = raw_input.strip()
    if not raw_input:
        return None  # No user text, allow through

    # 1. PII Scrubbing — modify the request in place
    scrubbed = raw_input
    for pattern, replacement in PII_PATTERNS:
        scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)

    # Update state with scrubbed input
    callback_context.state["scrubbed_input"] = scrubbed

    # 2. Prompt Injection Detection
    lower_input = raw_input.lower()
    for keyword in INJECTION_KEYWORDS:
        if keyword in lower_input:
            timestamp = datetime.now(timezone.utc).isoformat()
            callback_context.state["security_blocked"] = True
            callback_context.state["security_event"] = {
                "type": "PROMPT_INJECTION",
                "keyword": keyword,
                "timestamp": timestamp,
            }
            # Return a blocking response
            from google.adk.models.llm_response import LlmResponse
            return LlmResponse(
                content=genai_types.Content(
                    role="model",
                    parts=[genai_types.Part(
                        text=(
                            f"🛡️ **SECURITY ALERT**: Request blocked.\n\n"
                            f"Prohibited instruction detected: `{keyword}`\n"
                            f"This attempt has been logged at {timestamp}.\n\n"
                            f"AttriSense AI enforces strict access controls. "
                            f"Only authorized HR queries are permitted."
                        )
                    )]
                )
            )

    # 3. Role Authorization Check
    role = callback_context.state.get("requester_role", config.default_role)
    if role not in AUTHORIZED_ROLES:
        from google.adk.models.llm_response import LlmResponse
        return LlmResponse(
            content=genai_types.Content(
                role="model",
                parts=[genai_types.Part(
                    text=(
                        f"🔒 **ACCESS DENIED**: Role `{role}` is not authorized.\n\n"
                        f"Authorized roles: {sorted(AUTHORIZED_ROLES)}\n\n"
                        f"Please contact your HR Administrator for access."
                    )
                )]
            )
        )

    # 4. Salary masking for HR_ANALYST
    callback_context.state["mask_salary"] = (role == "HR_ANALYST")
    callback_context.state["security_cleared"] = True
    return None  # Allow the request through


# ─────────────────────────────────────────────────────────────────────────────
# RATE LIMITER — prevents 429 on Gemini free tier (5 req/min)
# ─────────────────────────────────────────────────────────────────────────────
_rate_lock = threading.Lock()
_last_llm_call_time: float = 0.0
RATE_LIMIT_GAP = 13.0  # seconds between sub-agent LLM calls


def rate_limit_callback(callback_context, llm_request):
    """Enforces minimum gap between LLM calls to stay within free-tier rate limits."""
    global _last_llm_call_time
    with _rate_lock:
        now = time.monotonic()
        elapsed = now - _last_llm_call_time
        if elapsed < RATE_LIMIT_GAP and _last_llm_call_time > 0:
            sleep_time = RATE_LIMIT_GAP - elapsed
            time.sleep(sleep_time)
        _last_llm_call_time = time.monotonic()
    return None  # Allow the LLM call through


# ─────────────────────────────────────────────────────────────────────────────
# SPECIALIST SUB-AGENTS
# ─────────────────────────────────────────────────────────────────────────────

signal_detection_agent = LlmAgent(
    name="signal_detection_agent",
    model=config.model,
    before_model_callback=rate_limit_callback,
    tools=[mcp_toolset],
    instruction="""You are the Signal Detection Agent for AttriSense AI.
Use the get_employee_data tool to retrieve the employee profile with all 14 signal parameters.
Analyze each signal against these risk thresholds:
  - Absenteeism > 15%: HIGH risk signal 🔴
  - Manager scorecard < 5.0: HIGH risk signal 🔴
  - Promotion gap > 3 years: HIGH risk signal 🔴
  - Internal job searches > 8: CRITICAL signal 🔴
  - Training count < 2/year: WARNING signal 🟡
  - Fresher + location mismatch: HIGH risk signal 🔴
  - High performer + salary_percentile < 40%: FLIGHT RISK 🔴
  - Collaboration index < 0.50 AND declining: WARNING 🟡
  - Sentiment score < -0.3: HIGH disengagement 🔴
  - Zero awards in last 12 months: WARNING 🟡

Return a structured analysis:
1. All 14 signals with traffic-light ratings (🔴 Critical / 🟠 High / 🟡 Moderate / 🟢 Low)
2. TOP 3 RISK DRIVERS with explanation
3. A 2-sentence plain-English SUMMARY of the employee's situation
""",
)

sentiment_analysis_agent = LlmAgent(
    name="sentiment_analysis_agent",
    model=config.model,
    before_model_callback=rate_limit_callback,
    tools=[mcp_toolset],
    instruction="""You are the Sentiment Analysis Agent for AttriSense AI.
Use the analyze_sentiment tool to process the employee's feedback text.
Then provide:
1. SENTIMENT SCORE: the numeric score from the tool (-1 to +1)
2. MOOD LABEL: the mood label from the tool
3. DETECTED THEMES: list the themes identified (e.g., burnout, career_stagnation)
4. INTERPRETATION: a 2-sentence empathetic interpretation of the employee's situation
   and what HR intervention this suggests.
Be empathetic. Focus on what the organization CAN DO, not on judging the employee.
""",
)

risk_scoring_agent = LlmAgent(
    name="risk_scoring_agent",
    model=config.model,
    before_model_callback=rate_limit_callback,
    tools=[mcp_toolset],
    instruction="""You are the Risk Scoring Agent for AttriSense AI.
Use the compute_risk_score tool to calculate the weighted Attrition Risk Score.
Then provide:
1. RISK SCORE: the exact score (e.g., 81.1%)
2. RISK LEVEL: CRITICAL / HIGH / MODERATE / LOW
3. PREDICTION WINDOW:
   - CRITICAL → "High probability within 3 months"
   - HIGH → "Elevated risk within 6 months"
   - MODERATE → "Moderate risk within 12 months"
   - LOW → "Stable — monitor quarterly"
4. TOP 5 CONTRIBUTING FACTORS with explanations
5. KEY INSIGHT: one sentence capturing the most important pattern
Be precise and data-driven.
""",
)

retention_advisor_agent = LlmAgent(
    name="retention_advisor_agent",
    model=config.model,
    before_model_callback=rate_limit_callback,
    tools=[mcp_toolset],
    instruction="""You are the Retention Advisor Agent for AttriSense AI.
Use the get_retention_playbook tool with the employee's risk level and top drivers.
Generate a ranked, actionable retention plan:
1. PRIORITY ACTIONS (top 3 — address within stated timeline):
   For each: Action | Owner (HR_ADMIN/MANAGER/LEADERSHIP) | Timeline | Expected Impact
2. SUPPORTING ACTIONS (next 2–3, within 60–90 days)
3. PREDICTED OUTCOME: "If these actions are taken within [timeframe],
   estimated risk reduction from [current]% to [projected]%."
Be specific and actionable. Every recommendation must be concrete, not generic.
""",
)


# ─────────────────────────────────────────────────────────────────────────────
# ORCHESTRATOR — coordinates all 4 specialist agents
# ─────────────────────────────────────────────────────────────────────────────

attrisense_orchestrator = LlmAgent(
    name="attrisense_orchestrator",
    model=config.model,
    before_model_callback=security_callback,
    tools=[
        AgentTool(agent=signal_detection_agent),
        AgentTool(agent=sentiment_analysis_agent),
        AgentTool(agent=risk_scoring_agent),
        AgentTool(agent=retention_advisor_agent),
    ],
    instruction="""You are AttriSense AI — an expert AI-powered Employee Attrition Intelligence system.
Built for LTTS Global Hackathon 2026.

Your purpose: Detect early leaver signals and provide actionable attrition risk intelligence to HR teams.

When asked to analyze an employee or department, follow this EXACT sequence:

STEP 1 — Call signal_detection_agent to retrieve and analyze all 14 behavioral signals.
STEP 2 — Call sentiment_analysis_agent to analyze the employee's feedback/engagement text.
STEP 3 — Call risk_scoring_agent to compute the weighted Attrition Risk Score.
STEP 4 — Call retention_advisor_agent to generate the retention intervention plan.

After all 4 agents complete, synthesize everything into this report format:

═══════════════════════════════════════════════════════
ATTRISENSE AI — EMPLOYEE ATTRITION RISK INTELLIGENCE
LTTS Global Hackathon 2026
═══════════════════════════════════════════════════════
EMPLOYEE: [name] | [department] | [tenure] years tenure
ANALYSIS DATE: [today's date]

📊 ATTRITION RISK SCORE: [score]% — [LEVEL]
⏰ PREDICTION WINDOW: [window]

🔴 TOP RISK DRIVERS:
[top 5 factors from risk_scoring_agent]

😔 SENTIMENT ANALYSIS:
Mood: [label] | Score: [value]
Themes: [detected themes]
[2-sentence empathetic interpretation]

📡 SIGNAL DASHBOARD:
[traffic-light summary of all 14 signals]

💡 RETENTION PLAN:
[priority actions from retention_advisor_agent]

🎯 KEY INSIGHT:
[most important pattern — the "aha" finding]

⚠️ HR ACTION REQUIRED: [YES — escalate immediately / MONITOR — schedule quarterly review]
═══════════════════════════════════════════════════════

IMPORTANT RULES:
- If risk score >= 60% (HIGH/CRITICAL): Flag "⚠️ IMMEDIATE HR ESCALATION REQUIRED"
- Never expose raw salary figures. Use percentile ranges instead.
- For department analysis (no specific employee_id), provide aggregate statistics.
- You can analyze ANY employee: type "analyze EMP001" or "analyze Engineering department"
- You can also answer HR questions about attrition patterns across the organization.

If no employee_id is provided, ask: "Which employee would you like to analyze?
Use their ID (e.g., EMP001) or department name (e.g., Engineering)."

Greet new sessions with: "👋 Welcome to AttriSense AI — Predicting Attrition Before It Happens.
I can analyze any employee's attrition risk using 14 behavioral and engagement signals.
Which employee or department would you like to assess today?"
""",
)

# ─────────────────────────────────────────────────────────────────────────────
# ADK ENTRY POINTS
# ─────────────────────────────────────────────────────────────────────────────
# ADK looks for either `root_agent` or `app` at module level
root_agent = attrisense_orchestrator
app = root_agent
