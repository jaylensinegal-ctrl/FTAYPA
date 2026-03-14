from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

from app.auth import ensure_demo_users
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers.athletes import router as athletes_router
from app.routers.auth import router as auth_router
from app.routers.baseline import router as baseline_router
from app.routers.competitions import router as competitions_router
from app.routers.development_system import router as development_system_router
from app.routers.memberships import router as memberships_router
from app.routers.performance import router as performance_router
from app.routers.rankings import router as rankings_router
from app.routers.visual_training import router as visual_training_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Auto-create tables for local proof-of-concept work. Production should use migrations.
    Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    ensure_local_schema_updates()
    seed_local_auth()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=settings.uploads_dir, check_dir=False), name="media")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(athletes_router)
app.include_router(auth_router)
app.include_router(baseline_router)
app.include_router(performance_router)
app.include_router(competitions_router)
app.include_router(development_system_router)
app.include_router(memberships_router)
app.include_router(rankings_router)
app.include_router(visual_training_router)


def ensure_local_schema_updates() -> None:
    inspector = inspect(engine)
    pending_statements = []

    if "membership_signups" in inspector.get_table_names():
        membership_columns = {column["name"] for column in inspector.get_columns("membership_signups")}

        if "payment_method" not in membership_columns:
            pending_statements.append("ALTER TABLE membership_signups ADD COLUMN payment_method VARCHAR(60) NOT NULL DEFAULT 'Stripe'")
        if "payment_status" not in membership_columns:
            pending_statements.append("ALTER TABLE membership_signups ADD COLUMN payment_status VARCHAR(60) NOT NULL DEFAULT 'Pending'")
        if "billing_country" not in membership_columns:
            pending_statements.append("ALTER TABLE membership_signups ADD COLUMN billing_country VARCHAR(80) NOT NULL DEFAULT 'United States'")
        if "currency" not in membership_columns:
            pending_statements.append("ALTER TABLE membership_signups ADD COLUMN currency VARCHAR(10) NOT NULL DEFAULT 'USD'")

    if "visual_training_sessions" in inspector.get_table_names():
        visual_columns = {column["name"] for column in inspector.get_columns("visual_training_sessions")}

        if "ai_form_score" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_form_score FLOAT")
        if "ai_posture_score" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_posture_score FLOAT")
        if "ai_balance_score" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_balance_score FLOAT")
        if "ai_analysis_profile" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_analysis_profile VARCHAR(80)")
        if "ai_analysis_summary" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_analysis_summary VARCHAR(1500)")
        if "ai_movement_flags" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_movement_flags VARCHAR(1000)")
        if "ai_analysis_version" not in visual_columns:
            pending_statements.append("ALTER TABLE visual_training_sessions ADD COLUMN ai_analysis_version VARCHAR(60)")

    for table_name in ("baseline_metrics", "performance_tests"):
        if table_name not in inspector.get_table_names():
            continue

        existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
        optional_metric_columns = {
            "standing_height": "FLOAT",
            "body_weight": "FLOAT",
            "speed_20yd": "FLOAT",
            "flying_10yd": "FLOAT",
            "medicine_ball_throw": "FLOAT",
            "l_drill": "FLOAT",
            "mobility_score": "FLOAT",
            "landing_control_score": "FLOAT",
            "single_leg_balance_left": "FLOAT",
            "single_leg_balance_right": "FLOAT",
            "squat_strength_ratio": "FLOAT",
            "yoyo_endurance": "FLOAT",
        }

        for column_name, column_type in optional_metric_columns.items():
            if column_name not in existing_columns:
                pending_statements.append(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    if not pending_statements:
        return

    with engine.begin() as connection:
        for statement in pending_statements:
            connection.execute(text(statement))


def seed_local_auth() -> None:
    if not settings.seed_demo_users:
        return
    with SessionLocal() as db:
        ensure_demo_users(db)
