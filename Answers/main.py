from fastapi import FastAPI
from Answers.generalQuery import router as general_router
from Answers.stockQuery import router as stock_router

app = FastAPI(title="Rimuru API Server")

# Register routers
app.include_router(general_router)
app.include_router(stock_router)


@app.get("/")
def read_root():
    return {"status": "online", "message": "Rimuru backend is running"}