from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from routes.events import router as events_router
from routes.users import router as users_router
from routes.auth import router as auth_router
from routes.organisers import router as organiser_router

app = FastAPI()
app.include_router(events_router, prefix="/api")
app.include_router(users_router,  prefix="/api")
app.include_router(auth_router,  prefix="/api")
app.include_router(organiser_router, prefix="/api")

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


# @app.exception_handler(RequestValidationError)
# def handle_validation_error(request: Request, exc: RequestValidationError):
#     return JSONResponse(status_code=400, content={"error": {"code": "INVALID_INPUT", "message": "Invalid format"}})