import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from errors import AppError
from routes import user_router, product_router, log_router

app = FastAPI()

@app.exception_handler(AppError)
async def app_exception_handler(exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.error,
        content=exc.detail,
    )


app.include_router(user_router)
app.include_router(product_router)
app.include_router(log_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)