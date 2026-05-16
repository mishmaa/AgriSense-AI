from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.analytics import DashboardAnalytics
from app.services.analytics_service import AnalyticsService
from app.services.farm_service import FarmService


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard/{farm_id}", response_model=DashboardAnalytics)
def dashboard(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DashboardAnalytics:
    FarmService(db).get_for_user(farm_id, current_user)
    return AnalyticsService(db).dashboard(farm_id)
