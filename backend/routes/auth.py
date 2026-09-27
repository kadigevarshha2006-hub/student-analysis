from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.schemas.auth import UserRegister, UserLogin, UserOut, TokenResponse
from backend.schemas.common import APIResponse
from backend.utils.security import (
    verify_password, get_password_hash, create_access_token, get_current_user
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Registers a new user and returns a signed JWT access token."""
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        full_name=user_in.full_name.strip(),
        email=user_in.email.lower(),
        hashed_password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return APIResponse(
        success=True,
        message="Account registered successfully.",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserOut.from_orm(user)
        )
    )

@router.post("/login", response_model=APIResponse[TokenResponse])
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """Authenticates a user and issues a JWT token."""
    user = db.query(User).filter(User.email == login_in.email.lower()).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is currently disabled."
        )

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return APIResponse(
        success=True,
        message="Login successful.",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserOut.from_orm(user)
        )
    )

@router.get("/me", response_model=APIResponse[UserOut])
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the authenticated user's profile details."""
    return APIResponse(
        success=True,
        message="Profile retrieved.",
        data=UserOut.from_orm(current_user)
    )
