from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.roles import require_role
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth", tags=["Auth"])

# 🔑 Register
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    print("Step 1: Request received")

    existing = db.query(User).filter(User.email == user.email).first()
    print("Step 2: Checked existing user")

    hashed = hash_password(user.password)
    print("Step 3: Password hashed")

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed,
        role="viewer"
    )
    print("Step 4: User object created")

    db.add(new_user)
    print("Step 5: Added to DB")

    db.commit()
    print("Step 6: Committed")

    db.refresh(new_user)
    print("Step 7: Refreshed")

    return {"message": "User created successfully"}

# @router.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     print("Incoming user:", user)
#     return {"message": "working"}



# 🔑 Login
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/users")
def get_users(user=Depends(require_role(["admin"]))):
    return {"message": "Only admin can see this"}