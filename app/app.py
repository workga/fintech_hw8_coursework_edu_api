from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.api.api import api_router
from app.database.db import init_db
from app.core.settings import app_settings


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI()
    
    init_db(testing)
    app.include_router(api_router, prefix='/api')


    @AuthJWT.load_config
    def get_config():
        return app_settings

    @app.exception_handler(AuthJWTException)
    def handle_authjwt_exception(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    return app
