from fastapi import FastAPI
import uvicorn
from config import get_settings
from routes.router import central_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(central_router, prefix="/v2")

origins = [
    "*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}

    
if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=get_settings().host,
        port=get_settings().port,
    )

