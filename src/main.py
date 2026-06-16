from fastapi import FastAPI

from src.db import engine
from src.db import Base
from src.routers.users import router as users_router
from src.routers.auth import router as auth_router
from src.routers.documents import router as doc_router
#from src.routers.data import router as data_router

#import src.models.user
#import src.models.role
#import src.models.permission
#import src.models.associations

app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(doc_router)
#app.include_router(data_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def hello():
    return {"message": "Hello"}
