from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Athlete(Base):
    __tablename__ = "athletes"

    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    primary_sport: Mapped[str] = mapped_column(String(100), nullable=False)
    secondary_sport: Mapped[Optional[str]] = mapped_column(String(100))
    team: Mapped[Optional[str]] = mapped_column(String(120))
    coach: Mapped[Optional[str]] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    baseline_metric: Mapped[Optional[BaselineMetric]] = relationship(back_populates="athlete", cascade="all, delete-orphan", uselist=False)
    performance_tests: Mapped[list[PerformanceTest]] = relationship(back_populates="athlete", cascade="all, delete-orphan")
    visual_training_sessions: Mapped[list[VisualTrainingSession]] = relationship(back_populates="athlete", cascade="all, delete-orphan")
    competition_results: Mapped[list[CompetitionResult]] = relationship(back_populates="athlete", cascade="all, delete-orphan")
    rankings: Mapped[list[AthleteRanking]] = relationship(back_populates="athlete", cascade="all, delete-orphan")
    pathway: Mapped[Optional[AthletePathway]] = relationship(back_populates="athlete", cascade="all, delete-orphan", uselist=False)
    training_plans: Mapped[list[TrainingPlan]] = relationship(back_populates="athlete", cascade="all, delete-orphan")
    session_logs: Mapped[list[TrainingSessionLog]] = relationship(back_populates="athlete", cascade="all, delete-orphan")
    assigned_users: Mapped[list[UserAccount]] = relationship(back_populates="athlete")


class BaselineMetric(Base):
    __tablename__ = "baseline_metrics"
    __table_args__ = (UniqueConstraint("athlete_id", name="uq_baseline_metrics_athlete_id"),)

    baseline_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    baseline_date: Mapped[date] = mapped_column(Date, nullable=False)
    standing_height: Mapped[Optional[float]] = mapped_column(Float)
    body_weight: Mapped[Optional[float]] = mapped_column(Float)
    speed_10yd: Mapped[float] = mapped_column(Float, nullable=False)
    speed_20yd: Mapped[Optional[float]] = mapped_column(Float)
    speed_40yd: Mapped[float] = mapped_column(Float, nullable=False)
    flying_10yd: Mapped[Optional[float]] = mapped_column(Float)
    vertical_jump: Mapped[float] = mapped_column(Float, nullable=False)
    broad_jump: Mapped[float] = mapped_column(Float, nullable=False)
    medicine_ball_throw: Mapped[Optional[float]] = mapped_column(Float)
    agility_shuttle: Mapped[float] = mapped_column(Float, nullable=False)
    l_drill: Mapped[Optional[float]] = mapped_column(Float)
    reaction_time: Mapped[float] = mapped_column(Float, nullable=False)
    pullups: Mapped[int] = mapped_column(Integer, nullable=False)
    pushups: Mapped[int] = mapped_column(Integer, nullable=False)
    mobility_score: Mapped[Optional[float]] = mapped_column(Float)
    landing_control_score: Mapped[Optional[float]] = mapped_column(Float)
    single_leg_balance_left: Mapped[Optional[float]] = mapped_column(Float)
    single_leg_balance_right: Mapped[Optional[float]] = mapped_column(Float)
    squat_strength_ratio: Mapped[Optional[float]] = mapped_column(Float)
    endurance_300yd: Mapped[float] = mapped_column(Float, nullable=False)
    yoyo_endurance: Mapped[Optional[float]] = mapped_column(Float)
    baseline_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="baseline_metric")


class PerformanceTest(Base):
    __tablename__ = "performance_tests"

    test_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    test_date: Mapped[date] = mapped_column(Date, nullable=False)
    standing_height: Mapped[Optional[float]] = mapped_column(Float)
    body_weight: Mapped[Optional[float]] = mapped_column(Float)
    speed_10yd: Mapped[float] = mapped_column(Float, nullable=False)
    speed_20yd: Mapped[Optional[float]] = mapped_column(Float)
    speed_40yd: Mapped[float] = mapped_column(Float, nullable=False)
    flying_10yd: Mapped[Optional[float]] = mapped_column(Float)
    vertical_jump: Mapped[float] = mapped_column(Float, nullable=False)
    broad_jump: Mapped[float] = mapped_column(Float, nullable=False)
    medicine_ball_throw: Mapped[Optional[float]] = mapped_column(Float)
    agility_shuttle: Mapped[float] = mapped_column(Float, nullable=False)
    l_drill: Mapped[Optional[float]] = mapped_column(Float)
    reaction_time: Mapped[float] = mapped_column(Float, nullable=False)
    pullups: Mapped[int] = mapped_column(Integer, nullable=False)
    pushups: Mapped[int] = mapped_column(Integer, nullable=False)
    mobility_score: Mapped[Optional[float]] = mapped_column(Float)
    landing_control_score: Mapped[Optional[float]] = mapped_column(Float)
    single_leg_balance_left: Mapped[Optional[float]] = mapped_column(Float)
    single_leg_balance_right: Mapped[Optional[float]] = mapped_column(Float)
    squat_strength_ratio: Mapped[Optional[float]] = mapped_column(Float)
    endurance_300yd: Mapped[float] = mapped_column(Float, nullable=False)
    yoyo_endurance: Mapped[Optional[float]] = mapped_column(Float)
    performance_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="performance_tests")


class CompetitionResult(Base):
    __tablename__ = "competition_results"

    result_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    event_name: Mapped[str] = mapped_column(String(150), nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    placement: Mapped[int] = mapped_column(Integer, nullable=False)
    points_earned: Mapped[int] = mapped_column(Integer, nullable=False)
    win_loss: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="competition_results")


class VisualTrainingSession(Base):
    __tablename__ = "visual_training_sessions"

    session_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    drill_name: Mapped[str] = mapped_column(String(150), nullable=False)
    video_url: Mapped[Optional[str]] = mapped_column(String(500))
    coach_notes: Mapped[Optional[str]] = mapped_column(String(1500))
    movement_quality: Mapped[int] = mapped_column(Integer, nullable=False)
    effort_level: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_level: Mapped[int] = mapped_column(Integer, nullable=False)
    focus_area: Mapped[Optional[str]] = mapped_column(String(120))
    tags: Mapped[Optional[str]] = mapped_column(String(500))
    ai_readiness_score: Mapped[float] = mapped_column(Float, nullable=False)
    ai_form_score: Mapped[Optional[float]] = mapped_column(Float)
    ai_posture_score: Mapped[Optional[float]] = mapped_column(Float)
    ai_balance_score: Mapped[Optional[float]] = mapped_column(Float)
    ai_analysis_profile: Mapped[Optional[str]] = mapped_column(String(80))
    ai_analysis_summary: Mapped[Optional[str]] = mapped_column(String(1500))
    ai_movement_flags: Mapped[Optional[str]] = mapped_column(String(1000))
    ai_analysis_version: Mapped[Optional[str]] = mapped_column(String(60))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="visual_training_sessions")


class AthleteRanking(Base):
    __tablename__ = "athlete_rankings"

    ranking_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False, unique=True)
    ranking_score: Mapped[float] = mapped_column(Float, nullable=False)
    tier_level: Mapped[str] = mapped_column(String(50), nullable=False)
    wing_level: Mapped[str] = mapped_column(String(50), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="rankings")


class MembershipSignup(Base):
    __tablename__ = "membership_signups"

    signup_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    athlete_last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    athlete_age: Mapped[int] = mapped_column(Integer, nullable=False)
    primary_sport: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_name: Mapped[str] = mapped_column(String(150), nullable=False)
    parent_email: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_phone: Mapped[str] = mapped_column(String(40), nullable=False)
    monthly_plan: Mapped[str] = mapped_column(String(120), nullable=False)
    monthly_amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(60), nullable=False, default="Stripe")
    payment_status: Mapped[str] = mapped_column(String(60), nullable=False, default="Pending")
    billing_country: Mapped[str] = mapped_column(String(80), nullable=False, default="United States")
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Active")
    consent_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[Optional[str]] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    waiver: Mapped[Optional[MembershipWaiver]] = relationship(back_populates="signup", cascade="all, delete-orphan", uselist=False)


class AthletePathway(Base):
    __tablename__ = "athlete_pathways"
    __table_args__ = (UniqueConstraint("athlete_id", name="uq_athlete_pathways_athlete_id"),)

    pathway_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    pathway_name: Mapped[str] = mapped_column(String(120), nullable=False)
    phase_name: Mapped[str] = mapped_column(String(120), nullable=False)
    primary_focus: Mapped[str] = mapped_column(String(120), nullable=False)
    secondary_focus: Mapped[Optional[str]] = mapped_column(String(120))
    readiness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    readiness_status: Mapped[str] = mapped_column(String(60), nullable=False, default="Building")
    next_review_date: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="pathway")


class MembershipWaiver(Base):
    __tablename__ = "membership_waivers"
    __table_args__ = (UniqueConstraint("signup_id", name="uq_membership_waivers_signup_id"),)

    waiver_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signup_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("membership_signups.signup_id", ondelete="CASCADE"), nullable=False)
    waiver_version: Mapped[str] = mapped_column(String(40), nullable=False, default="FTA-WAIVER-1.0")
    parent_guardian_name: Mapped[str] = mapped_column(String(150), nullable=False)
    guardian_relationship: Mapped[str] = mapped_column(String(80), nullable=False)
    parent_signature: Mapped[str] = mapped_column(String(150), nullable=False)
    athlete_assent_name: Mapped[Optional[str]] = mapped_column(String(150))
    emergency_contact_name: Mapped[str] = mapped_column(String(150), nullable=False)
    emergency_contact_phone: Mapped[str] = mapped_column(String(40), nullable=False)
    emergency_contact_relationship: Mapped[str] = mapped_column(String(80), nullable=False)
    medical_notes: Mapped[Optional[str]] = mapped_column(String(1500))
    has_medical_clearance: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    liability_waiver_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    emergency_care_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    training_policies_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    privacy_policy_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    electronic_signature_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    media_release_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    signed_ip_address: Mapped[Optional[str]] = mapped_column(String(80))
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    signup: Mapped[MembershipSignup] = relationship(back_populates="waiver")


class TrainingPlan(Base):
    __tablename__ = "training_plans"

    plan_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    weekly_sessions_target: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    status: Mapped[str] = mapped_column(String(60), nullable=False, default="Active")
    primary_focus: Mapped[str] = mapped_column(String(120), nullable=False)
    secondary_focus: Mapped[Optional[str]] = mapped_column(String(120))
    goals_summary: Mapped[str] = mapped_column(String(1200), nullable=False)
    coach_recommendation: Mapped[Optional[str]] = mapped_column(String(1200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="training_plans")
    session_logs: Mapped[list[TrainingSessionLog]] = relationship(back_populates="training_plan")


class TrainingSessionLog(Base):
    __tablename__ = "training_session_logs"

    session_log_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    athlete_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="CASCADE"), nullable=False)
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("training_plans.plan_id", ondelete="SET NULL"))
    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    session_type: Mapped[str] = mapped_column(String(120), nullable=False)
    planned_focus: Mapped[str] = mapped_column(String(150), nullable=False)
    workload_score: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    attendance_status: Mapped[str] = mapped_column(String(60), nullable=False, default="Attended")
    completion_status: Mapped[str] = mapped_column(String(60), nullable=False, default="Completed")
    coach_notes: Mapped[Optional[str]] = mapped_column(String(1500))
    athlete_feedback: Mapped[Optional[str]] = mapped_column(String(1000))
    soreness_level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    confidence_level: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    athlete: Mapped[Athlete] = relationship(back_populates="session_logs")
    training_plan: Mapped[Optional[TrainingPlan]] = relationship(back_populates="session_logs")


class UserAccount(Base):
    __tablename__ = "user_accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    athlete_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="SET NULL"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    athlete: Mapped[Optional[Athlete]] = relationship(back_populates="assigned_users")
    sessions: Mapped[list[AuthSession]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sent_invites: Mapped[list[AccountInvite]] = relationship(back_populates="invited_by")


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    session_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped[UserAccount] = relationship(back_populates="sessions")


class AccountInvite(Base):
    __tablename__ = "account_invites"

    invite_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    athlete_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("athletes.athlete_id", ondelete="SET NULL"))
    invited_by_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("user_accounts.user_id", ondelete="CASCADE"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    athlete: Mapped[Optional[Athlete]] = relationship()
    invited_by: Mapped[UserAccount] = relationship(back_populates="sent_invites")
