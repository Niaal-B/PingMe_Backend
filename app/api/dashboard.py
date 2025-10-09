from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user,bearer_scheme
from app.db.models import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard_data(
    current_user: User = Depends(get_current_user) 
):
    """
    Returns personalized data only if the user is successfully authenticated.
    """
    return {
        "message": f"Welcome to the PingMe Dashboard, {current_user.username}!",
        "user_id": current_user.id,
        "email": current_user.email,
        "status": "Authenticated"
    }