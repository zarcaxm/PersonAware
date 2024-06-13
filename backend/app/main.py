from fastapi import FastAPI
from app.routes import file_upload

app = FastAPI()

app.include_router(file_upload.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090, log_level="info")
