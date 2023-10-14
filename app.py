"""
App
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/healthcheck")
async def health_check():
    """
    Health Check
    """
    return {"status": "OK", "message": "Up & Running!"}
