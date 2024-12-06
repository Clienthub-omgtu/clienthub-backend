from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_admin.contrib.sqla import Admin

from fastapi_pagination import add_pagination
from uvicorn import run

from src.config import Settings, get_settings
from src.api import list_of_routes
from src.admin_views import list_of_views
from src.db.connection import get_sync_engine


def bind_routes(application: FastAPI, setting: Settings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def bind_models_admin(admin_app: Admin) -> None:
    """
    Bind all models to admin panel.
    """
    for view in list_of_views:
        admin_app.add_view(view(model=view.model))


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """

    tags_metadata = [
        {
            "name": "Application Health",
            "description": "API health check.",
        },
    ]

    settings = get_settings()
    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        docs_url="/api/swagger",
        openapi_url="/api/openapi",
        version=settings.APP_VERSION,
        openapi_tags=tags_metadata,
    )
    bind_routes(application, settings)
    add_pagination(application)
    application.state.settings = settings
    return application


app = get_app()

admin_app = Admin(get_sync_engine(), title="ClientHub Admin")
bind_models_admin(admin_app=admin_app)
admin_app.mount_to(app)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "app.__main__:app",
        host=settings_for_application.APP_HOST,
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["app"],
        log_level="debug",
    )
