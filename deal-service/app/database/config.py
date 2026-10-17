from app.config import settings


TORTOISE_ORM = {
    "connections": {
        "default": settings.database_dsn_local if settings.is_local else settings.database_dsn
    },
    "apps": {
        "models": {
            "models": ["app.database.models"],
            "default_connection": "default",
            "migrations": "app.migrations"
        },
    },
}