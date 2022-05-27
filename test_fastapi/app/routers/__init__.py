from config.configs import api
from .auth import user

api.include_router(user.router)