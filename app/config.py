import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")


@dataclass
class RiskThresholds:
    """Risk level thresholds for Attrition Risk Score."""
    critical: float = 80.0    # >= 80% → CRITICAL → triggers HITL human review
    high: float = 60.0        # 60–79% → HIGH → immediate manager intervention
    moderate: float = 30.0    # 30–59% → MODERATE → proactive check-in


@dataclass
class SignalWeightages:
    """14 attrition signal parameter weightages — must sum to 1.0."""
    absenteeism: float = 0.12
    sentiment_score: float = 0.10
    performance_trend: float = 0.10
    compensation_gap: float = 0.10
    internal_job_searches: float = 0.08
    manager_scorecard: float = 0.08
    promotion_gap: float = 0.08
    meeting_participation: float = 0.06
    collaboration_index: float = 0.06
    training_activity: float = 0.06
    recognition_count: float = 0.06
    location_mismatch: float = 0.05
    cross_functional_work: float = 0.03
    team_social: float = 0.02


@dataclass
class AgentConfig:
    # Agent model — reads from GEMINI_MODEL env var.
    # Default: gemini-2.5-flash. DO NOT use gemini-1.5-* (retired, returns 404).
    # For tighter free-tier quota: gemini-2.5-flash-lite
    model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    mcp_server_port: int = 8090
    max_iterations: int = 5
    pii_redaction_enabled: bool = True
    injection_detection_enabled: bool = True
    default_role: str = "HR_ANALYST"
    thresholds: RiskThresholds = field(default_factory=RiskThresholds)
    weightages: SignalWeightages = field(default_factory=SignalWeightages)


config = AgentConfig()
