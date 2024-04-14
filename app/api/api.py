from fastapi import APIRouter

from .tag import routers as tag_routers
from .banner import routers as banner_routers
from .feature import routers as feature_routers
from .user_banner import routers as user_banner_routes
from .authentication import routerts as authentication_routes

routers = APIRouter()
routers.include_router(tag_routers.router)
routers.include_router(banner_routers.router)
routers.include_router(feature_routers.router)
routers.include_router(user_banner_routes.router)
routers.include_router(authentication_routes.router)
