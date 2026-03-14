from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Iterable, Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AccountInvite, Athlete, AuthSession, UserAccount

AUTH_SESSION_DAYS = 14
INVITE_EXPIRY_DAYS = 7
SUPPORTED_ROLES = {"coach", "parent", "athlete", "admin"}
DEMO_PASSWORD = "FlightTime123!"


def _utc_now() -> datetime:
    return datetime.utcnow()


def hash_password(password: str, salt: Optional[str] = None) -> str:
    normalized_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), normalized_salt.encode("utf-8"), 120000)
    return f"{normalized_salt}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        salt, expected = encoded.split("$", 1)
    except ValueError:
        return False
    computed = hash_password(password, salt).split("$", 1)[1]
    return secrets.compare_digest(computed, expected)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_invite_token() -> str:
    return secrets.token_urlsafe(24)


def create_session(db: Session, user: UserAccount) -> str:
    token = secrets.token_urlsafe(32)
    session = AuthSession(
        user_id=user.user_id,
        token_hash=hash_token(token),
        expires_at=_utc_now() + timedelta(days=AUTH_SESSION_DAYS),
        last_used_at=_utc_now(),
    )
    db.add(session)
    db.commit()
    return token


def revoke_session(db: Session, token: str) -> None:
    session = db.scalar(select(AuthSession).where(AuthSession.token_hash == hash_token(token)))
    if session is None or session.revoked_at is not None:
        return
    session.revoked_at = _utc_now()
    db.commit()


def get_user_by_token(db: Session, token: str) -> UserAccount:
    session = db.scalar(
        select(AuthSession)
        .where(AuthSession.token_hash == hash_token(token))
        .order_by(AuthSession.created_at.desc())
    )
    if session is None or session.revoked_at is not None or session.expires_at <= _utc_now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please sign in again.")

    user = session.user
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive.")

    session.last_used_at = _utc_now()
    db.commit()
    return user


def get_current_user(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> UserAccount:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in to continue.")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in to continue.")
    return get_user_by_token(db, token)


def require_roles(*roles: str):
    normalized_roles = {role.lower() for role in roles}

    def dependency(user: UserAccount = Depends(get_current_user)) -> UserAccount:
        if user.role.lower() not in normalized_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this area.")
        return user

    return dependency


def ensure_athlete_access(user: UserAccount, athlete_id: uuid.UUID) -> None:
    if user.role.lower() in {"coach", "admin"}:
        return
    if user.athlete_id != athlete_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this athlete.")


def get_visible_athletes_query(user: UserAccount):
    base = select(Athlete)
    if user.role.lower() in {"coach", "admin"}:
        return base
    if user.athlete_id is None:
        return base.where(Athlete.athlete_id == uuid.uuid4())
    return base.where(Athlete.athlete_id == user.athlete_id)


def ensure_demo_users(db: Session) -> None:
    existing = {
        user.email: user
        for user in db.scalars(select(UserAccount))
    }
    first_athlete = db.scalar(select(Athlete).order_by(Athlete.created_at.asc()))

    demo_definitions = [
        ("coach@flighttime.test", "coach", "FTA Coach Command", None),
        ("parent@flighttime.test", "parent", "FTA Parent View", first_athlete.athlete_id if first_athlete else None),
        ("athlete@flighttime.test", "athlete", "FTA Athlete View", first_athlete.athlete_id if first_athlete else None),
        ("admin@flighttime.test", "admin", "FTA Admin Control", None),
    ]

    changed = False
    for email, role, display_name, athlete_id in demo_definitions:
        account = existing.get(email)
        if account is None:
            db.add(
                UserAccount(
                    email=email,
                    password_hash=hash_password(DEMO_PASSWORD),
                    role=role,
                    display_name=display_name,
                    athlete_id=athlete_id,
                )
            )
            changed = True
            continue

        if athlete_id is not None and account.athlete_id is None and account.role in {"parent", "athlete"}:
            account.athlete_id = athlete_id
            changed = True

    if changed:
        db.commit()


def validate_role(role: str) -> str:
    normalized = role.strip().lower()
    if normalized not in SUPPORTED_ROLES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported role")
    return normalized


def can_invite_role(inviter_role: str, target_role: str) -> bool:
    inviter = inviter_role.lower()
    target = target_role.lower()
    if inviter == "admin":
        return target in SUPPORTED_ROLES
    if inviter == "coach":
        return target in {"parent", "athlete", "coach"}
    return False


def get_invite_by_token(db: Session, token: str) -> AccountInvite:
    invite = db.scalar(select(AccountInvite).where(AccountInvite.token_hash == hash_token(token)))
    if invite is None or invite.revoked_at is not None or invite.accepted_at is not None or invite.expires_at <= _utc_now():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite is no longer available.")
    return invite


def is_staff_role(role: str) -> bool:
    return role.lower() in {"coach", "admin"}


def can_view_coach_tools(role: str) -> bool:
    return is_staff_role(role)


def visible_sections_for_role(role: str) -> Iterable[str]:
    if can_view_coach_tools(role):
        return ("Overview", "Development", "Coach Tools")
    return ("Overview", "Development")
