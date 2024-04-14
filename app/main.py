from fastapi import FastAPI

from api.api import routers

app = FastAPI()
app.include_router(routers)
