from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AthleteBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    age: Optional[int] = Field(default=None, ge=5, le=25)
    height: float = Field(gt=0)
    weight: float = Field(gt=0)
    primary_sport: str = Field(min_length=1, max_length=100)
    secondary_sport: Optional[str] = Field(default=None, max_length=100)
    team: Optional[str] = Field(default=None, max_length=120)
    coach: Optional[str] = Field(default=None, max_length=120)


class AthleteCreate(AthleteBase):
    pass


class AthleteRead(AthleteBase):
    athlete_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AthleticMetricsInput(BaseModel):
    standing_height: Optional[float] = Field(default=None, gt=0)
    body_weight: Optional[float] = Field(default=None, gt=0)
    speed_10yd: float = Field(gt=0)
    speed_20yd: Optional[float] = Field(default=None, gt=0)
    speed_40yd: float = Field(gt=0)
    flying_10yd: Optional[float] = Field(default=None, gt=0)
    vertical_jump: float = Field(gt=0)
    broad_jump: float = Field(gt=0)
    medicine_ball_throw: Optional[float] = Field(default=None, gt=0)
    agility_shuttle: float = Field(gt=0)
    l_drill: Optional[float] = Field(default=None, gt=0)
    reaction_time: float = Field(gt=0)
    pullups: int = Field(ge=0)
    pushups: int = Field(ge=0)
    mobility_score: Optional[float] = Field(default=None, ge=1, le=10)
    landing_control_score: Optional[float] = Field(default=None, ge=1, le=10)
    single_leg_balance_left: Optional[float] = Field(default=None, gt=0)
    single_leg_balance_right: Optional[float] = Field(default=None, gt=0)
    squat_strength_ratio: Optional[float] = Field(default=None, gt=0)
    endurance_300yd: float = Field(gt=0)
    yoyo_endurance: Optional[float] = Field(default=None, gt=0)


class BaselineCreate(AthleticMetricsInput):
    athlete_id: uuid.UUID
    baseline_date: date


class BaselineRead(BaselineCreate):
    baseline_id: uuid.UUID
    baseline_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PerformanceTestCreate(AthleticMetricsInput):
    athlete_id: uuid.UUID
    test_date: date


class PerformanceTestRead(PerformanceTestCreate):
    test_id: uuid.UUID
    performance_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompetitionResultCreate(BaseModel):
    athlete_id: uuid.UUID
    event_name: str = Field(min_length=1, max_length=150)
    event_date: date
    placement: int = Field(ge=1)
    points_earned: Optional[int] = Field(default=None, ge=0)
    win_loss: str = Field(min_length=3, max_length=10)

    @field_validator("win_loss")
    @classmethod
    def normalize_win_loss(cls, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in {"WIN", "LOSS"}:
            raise ValueError("win_loss must be WIN or LOSS")
        return normalized


class CompetitionResultRead(CompetitionResultCreate):
    result_id: uuid.UUID
    points_earned: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AthleteRankingRead(BaseModel):
    ranking_id: uuid.UUID
    athlete_id: uuid.UUID
    ranking_score: float
    tier_level: str
    wing_level: str
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class RankingBoardEntryRead(BaseModel):
    athlete_id: uuid.UUID
    athlete_name: str
    primary_sport: str
    ranking_score: float
    tier_level: str
    wing_level: str
    last_updated: datetime


class MembershipSignupCreate(BaseModel):
    athlete_first_name: str = Field(min_length=1, max_length=100)
    athlete_last_name: str = Field(min_length=1, max_length=100)
    athlete_age: int = Field(ge=5, le=17)
    primary_sport: str = Field(min_length=1, max_length=100)
    parent_name: str = Field(min_length=1, max_length=150)
    parent_email: str = Field(min_length=3, max_length=200)
    parent_phone: str = Field(min_length=7, max_length=40)
    monthly_plan: str = Field(min_length=1, max_length=120)
    monthly_amount: float = Field(gt=0)
    payment_method: str = Field(min_length=1, max_length=60)
    payment_status: str = Field(default="Pending", min_length=1, max_length=60)
    billing_country: str = Field(min_length=1, max_length=80)
    currency: str = Field(min_length=3, max_length=10)
    consent_accepted: bool
    notes: Optional[str] = Field(default=None, max_length=1000)


class MembershipWaiverCreate(BaseModel):
    waiver_version: str = Field(default="FTA-WAIVER-1.0", min_length=3, max_length=40)
    parent_guardian_name: str = Field(min_length=1, max_length=150)
    guardian_relationship: str = Field(min_length=1, max_length=80)
    parent_signature: str = Field(min_length=1, max_length=150)
    athlete_assent_name: Optional[str] = Field(default=None, max_length=150)
    emergency_contact_name: str = Field(min_length=1, max_length=150)
    emergency_contact_phone: str = Field(min_length=7, max_length=40)
    emergency_contact_relationship: str = Field(min_length=1, max_length=80)
    medical_notes: Optional[str] = Field(default=None, max_length=1500)
    has_medical_clearance: bool
    liability_waiver_accepted: bool
    emergency_care_accepted: bool
    training_policies_accepted: bool
    privacy_policy_accepted: bool
    electronic_signature_accepted: bool
    media_release_accepted: bool = False


class MembershipSignupWithWaiverCreate(MembershipSignupCreate):
    waiver: MembershipWaiverCreate


class MembershipWaiverRead(MembershipWaiverCreate):
    waiver_id: uuid.UUID
    signup_id: uuid.UUID
    signed_ip_address: Optional[str]
    signed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MembershipSignupRead(MembershipSignupCreate):
    signup_id: uuid.UUID
    status: str
    created_at: datetime
    waiver: Optional[MembershipWaiverRead] = None

    model_config = ConfigDict(from_attributes=True)


class MembershipCheckoutSessionRequest(BaseModel):
    signup_id: uuid.UUID


class MembershipCheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


class MembershipPaymentUpdateRequest(BaseModel):
    payment_status: str = Field(min_length=1, max_length=60)


class CompetitionRecordSummary(BaseModel):
    total_events: int
    total_points: int
    average_points: float
    wins: int
    losses: int
    podium_finishes: int


class VisualTrainingSessionCreate(BaseModel):
    athlete_id: uuid.UUID
    session_date: date
    drill_name: str = Field(min_length=1, max_length=150)
    video_url: Optional[str] = Field(default=None, max_length=500)
    coach_notes: Optional[str] = Field(default=None, max_length=1500)
    movement_quality: int = Field(ge=1, le=10)
    effort_level: int = Field(ge=1, le=10)
    confidence_level: int = Field(ge=1, le=10)
    focus_area: Optional[str] = Field(default=None, max_length=120)
    tags: list[str] = Field(default_factory=list)
    ai_form_score: Optional[float] = None
    ai_posture_score: Optional[float] = None
    ai_balance_score: Optional[float] = None
    ai_analysis_profile: Optional[str] = Field(default=None, max_length=80)
    ai_analysis_summary: Optional[str] = Field(default=None, max_length=1500)
    ai_movement_flags: list[str] = Field(default_factory=list)
    ai_analysis_version: Optional[str] = Field(default=None, max_length=60)


class VideoUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1, max_length=120)
    data_base64: str = Field(min_length=1)


class VideoUploadResponse(BaseModel):
    file_url: str
    file_name: str
    content_type: str
    size_bytes: int


class VisualTrainingSessionRead(BaseModel):
    session_id: uuid.UUID
    athlete_id: uuid.UUID
    session_date: date
    drill_name: str
    video_url: Optional[str]
    coach_notes: Optional[str]
    movement_quality: int
    effort_level: int
    confidence_level: int
    focus_area: Optional[str]
    tags: list[str]
    ai_readiness_score: float
    ai_form_score: Optional[float]
    ai_posture_score: Optional[float]
    ai_balance_score: Optional[float]
    ai_analysis_profile: Optional[str]
    ai_analysis_summary: Optional[str]
    ai_movement_flags: list[str]
    ai_analysis_version: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VisualTrainingSummary(BaseModel):
    total_sessions: int
    latest_session_date: Optional[date]
    average_movement_quality: float
    average_effort: float
    average_confidence: float
    average_ai_readiness_score: float
    latest_focus_area: Optional[str]
    latest_tags: list[str]


class AthletePathwayRead(BaseModel):
    pathway_id: uuid.UUID
    athlete_id: uuid.UUID
    pathway_name: str
    phase_name: str
    primary_focus: str
    secondary_focus: Optional[str]
    readiness_score: float
    readiness_status: str
    next_review_date: Optional[date]

    model_config = ConfigDict(from_attributes=True)


class TrainingPlanCreate(BaseModel):
    athlete_id: uuid.UUID
    title: str = Field(min_length=1, max_length=150)
    weekly_sessions_target: int = Field(ge=1, le=7)
    status: str = Field(default="Active", min_length=1, max_length=60)
    primary_focus: str = Field(min_length=1, max_length=120)
    secondary_focus: Optional[str] = Field(default=None, max_length=120)
    goals_summary: str = Field(min_length=1, max_length=1200)
    coach_recommendation: Optional[str] = Field(default=None, max_length=1200)


class TrainingPlanRead(TrainingPlanCreate):
    plan_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainingTemplateSession(BaseModel):
    day_label: str
    session_type: str
    focus: str
    drills: list[str]


class TrainingTemplateSummary(BaseModel):
    template_name: str
    age_band: str
    sport_track: str
    sessions: list[TrainingTemplateSession]


class TrainingSessionLogCreate(BaseModel):
    athlete_id: uuid.UUID
    plan_id: Optional[uuid.UUID] = None
    session_date: date
    session_type: str = Field(min_length=1, max_length=120)
    planned_focus: str = Field(min_length=1, max_length=150)
    workload_score: int = Field(ge=1, le=10)
    attendance_status: str = Field(min_length=1, max_length=60)
    completion_status: str = Field(min_length=1, max_length=60)
    coach_notes: Optional[str] = Field(default=None, max_length=1500)
    athlete_feedback: Optional[str] = Field(default=None, max_length=1000)
    soreness_level: int = Field(ge=1, le=10)
    confidence_level: int = Field(ge=1, le=10)


class TrainingSessionLogRead(TrainingSessionLogCreate):
    session_log_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionOperatingSummary(BaseModel):
    planned_sessions: int
    attended_sessions: int
    completed_sessions: int
    attendance_rate: float
    completion_rate: float
    average_workload: float
    average_soreness: float
    average_confidence: float
    recent_coach_note: Optional[str]


class MetricCoverageGroup(BaseModel):
    name: str
    captured: int
    total: int
    status: str
    missing: list[str]


class BaselineCoverageSummary(BaseModel):
    completion_percent: float
    coverage_note: str
    critical_missing: list[str]
    recommended_missing: list[str]
    groups: list[MetricCoverageGroup]


class DevelopmentInsightSummary(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    readiness_flags: list[str]
    training_suggestions: list[str]
    injury_risk_indicators: list[str]
    matchup_recommendations: list[str]
    next_best_action: str
    coach_summary: str
    parent_summary: str
    athlete_summary: str
    admin_summary: str


class ProgressionSummary(BaseModel):
    current_stage: str
    next_stage: str
    progress_percent: float
    promotion_readiness: str
    milestone_checks: list[str]


class ReviewCycleSummary(BaseModel):
    cadence_label: str
    next_review_focus: str
    checklist: list[str]
    recommended_review_window_days: int


class PlanAdjustmentSummary(BaseModel):
    adjustment_mode: str
    reason: str
    session_target: int
    focus_shift: str
    coach_action_items: list[str]


class BuildAttributeRating(BaseModel):
    category: str
    rating: int
    trend: str


class ProgressBadge(BaseModel):
    name: str
    tier: str
    progress_percent: float


class AthleteBuildProgressionSummary(BaseModel):
    build_name: str
    archetype: str
    takeoff_level: int
    overall_rating: int
    xp_progress_percent: float
    next_unlock: str
    build_focus: str
    attributes: list[BuildAttributeRating]
    badges: list[ProgressBadge]


class DevelopmentProfileResponse(BaseModel):
    athlete: AthleteRead
    baseline_score: float
    latest_performance_score: float
    improvement_score: float
    development_velocity: float
    days_since_baseline: int
    competition_record: CompetitionRecordSummary
    ranking_position: Optional[int]
    wing_level: Optional[str]
    tier_level: Optional[str]
    latest_test_date: Optional[date]
    baseline_coverage: BaselineCoverageSummary
    visual_training_summary: VisualTrainingSummary
    pathway: AthletePathwayRead
    active_training_plan: TrainingPlanRead
    training_template: TrainingTemplateSummary
    recent_session_logs: list[TrainingSessionLogRead]
    session_operating_summary: SessionOperatingSummary
    insights: DevelopmentInsightSummary
    progression: ProgressionSummary
    review_cycle: ReviewCycleSummary
    plan_adjustment: PlanAdjustmentSummary
    athlete_build: AthleteBuildProgressionSummary


class AuthLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=200)
    password: str = Field(min_length=6, max_length=120)


class AuthUserRead(BaseModel):
    user_id: uuid.UUID
    email: str
    role: str
    display_name: str
    athlete_id: Optional[uuid.UUID]

    model_config = ConfigDict(from_attributes=True)


class AuthLoginResponse(BaseModel):
    token: str
    user: AuthUserRead


class InviteCreateRequest(BaseModel):
    email: str = Field(min_length=3, max_length=200)
    role: str = Field(min_length=3, max_length=30)
    display_name: str = Field(min_length=1, max_length=150)
    athlete_id: Optional[uuid.UUID] = None


class InviteRead(BaseModel):
    invite_id: uuid.UUID
    email: str
    role: str
    display_name: str
    athlete_id: Optional[uuid.UUID]
    invited_by_user_id: uuid.UUID
    expires_at: datetime
    accepted_at: Optional[datetime]
    revoked_at: Optional[datetime]
    created_at: datetime
    invite_link: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class InviteAcceptRequest(BaseModel):
    token: str = Field(min_length=12, max_length=255)
    password: str = Field(min_length=8, max_length=120)


class InvitePreviewResponse(BaseModel):
    email: str
    role: str
    display_name: str
    athlete_id: Optional[uuid.UUID]
    expires_at: datetime
