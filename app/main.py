from fastapi import FastAPI


from app.api.v1.tasks import router as tasks_router

app = FastAPI(
    title="Task Service",
    description="Асинхронный сервис)",
    version="1.0.0"
)


app.include_router(tasks_router)

@app.get("/")
async def root():
    return {"message": "Task Service запущен! Перейди на /docs"}