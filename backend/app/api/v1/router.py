from fastapi import APIRouter

from app.api.v1.routes import (
    ai,
    analytics,
    auth,
    chatbot,
    crop_calendar,
    drone,
    farms,
    irrigation,
    marketplace,
    notifications,
    sensors,
    users,
    weather,
)


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(farms.router)
api_router.include_router(sensors.router)
api_router.include_router(irrigation.router)
api_router.include_router(ai.router)
api_router.include_router(ai.disease_router)
api_router.include_router(notifications.router)
api_router.include_router(marketplace.router)
api_router.include_router(analytics.router)
api_router.include_router(weather.router)
api_router.include_router(chatbot.router)
api_router.include_router(drone.router)
api_router.include_router(crop_calendar.router)
