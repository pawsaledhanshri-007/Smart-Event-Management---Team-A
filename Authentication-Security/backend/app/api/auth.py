from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api.deps import get_db, get_current_user
from app.core import security
from app.core.config import settings
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token


router = APIRouter()


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new participant.
    """

    normalized_email = str(user_in.email).strip().lower()
    user = db.query(User).filter(
        User.email == normalized_email
    ).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system.",
        )

    user = User(
    email=normalized_email,
    name=user_in.name,
    phone=user_in.phone,
    age=user_in.age,
    college=user_in.college,
    password_hash=security.get_password_hash(user_in.password),
    role=UserRole.PARTICIPANT.value
)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    """
    Email/password login with strict Admin/User account-type isolation.
    """
    selected_role = role.strip().lower()
    selected_role = {
        "user": UserRole.PARTICIPANT.value,
        "participant": UserRole.PARTICIPANT.value,
        "admin": UserRole.ADMIN.value,
    }.get(selected_role)
    if selected_role is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Choose either Admin or User.",
        )

    user = db.query(User).filter(
        User.email == username.strip().lower()
    ).first()

    if not user or not security.verify_password(
        password,
        user.password_hash
    ) or user.role != selected_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password does not match the selected account type.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account is disabled.",
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = security.create_access_token(
        subject=user.id,
        role=user.role,
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user.
    """

    return current_user