from fastapi import APIRouter, Depends
from app.dependencies.roles import require_role

router = APIRouter(prefix="/users", tags=["Users"])


# 🔴 Admin only
@router.get("/")
def get_users(user = Depends(require_role(["admin"]))):
    return {"message": "All users"}


# 🔴 Admin only
@router.patch("/{id}")
def update_user(id: int, user = Depends(require_role(["admin"]))):
    return {"message": f"User {id} updated"}