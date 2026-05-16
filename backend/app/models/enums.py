from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    FARMER = "farmer"
    AGRONOMIST = "agronomist"
    OPERATOR = "operator"


class IrrigationMode(StrEnum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SCHEDULED = "scheduled"


class SensorType(StrEnum):
    SOIL_MOISTURE = "soil_moisture"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WATER_TANK = "water_tank"
    PH = "ph"
    NPK = "npk"
    LIGHT = "light"
    MULTI = "multi"


class SensorStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    FAULT = "fault"


class IrrigationStatus(StrEnum):
    STARTED = "started"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FAILED = "failed"


class RecommendationType(StrEnum):
    CROP = "crop"
    FERTILIZER = "fertilizer"
    YIELD = "yield"
    IRRIGATION = "irrigation"
    WEATHER_RISK = "weather_risk"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class NotificationType(StrEnum):
    SENSOR = "sensor"
    IRRIGATION = "irrigation"
    WEATHER = "weather"
    AI = "ai"
    MARKETPLACE = "marketplace"
    SYSTEM = "system"


class NotificationChannel(StrEnum):
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class MarketplaceCategory(StrEnum):
    SEEDS = "seeds"
    FERTILIZER = "fertilizer"
    EQUIPMENT = "equipment"
    PRODUCE = "produce"
    SERVICE = "service"


class MarketplaceStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    ARCHIVED = "archived"


class ChatRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MissionStatus(StrEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CalendarActivityType(StrEnum):
    SOWING = "sowing"
    IRRIGATION = "irrigation"
    FERTILIZING = "fertilizing"
    SPRAYING = "spraying"
    HARVESTING = "harvesting"
    INSPECTION = "inspection"


class CalendarStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    OVERDUE = "overdue"
