from fastapi import FastAPI, Response, status
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import json
from users_endpoint import users_info_router
import db_util

app = FastAPI()
app.include_router(users_info_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def get_health():
    connection = db_util.DbUsersSystem.get_connection()
    t = str(datetime.now())
    if connection:
        db_connection_status = True
        status_code = status.HTTP_200_OK
        health = "Good"
    else:
        db_connection_status = False
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        health = "Not good"

    msg = {
            "name": "Users-Microservice",
            "health": health,
            "DB connection": db_connection_status,
            "at time": t
           }

    result = Response(json.dumps(msg), status_code=status_code)

    return result
