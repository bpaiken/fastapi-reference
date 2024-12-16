from src.fastapi_reference.settings.app_settings import _AppSettings

_app_settings = _AppSettings()

# Nested settings here (to be imported in other modules)
database_settings = _app_settings.database_settings